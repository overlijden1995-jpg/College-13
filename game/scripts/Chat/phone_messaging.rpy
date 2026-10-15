# ============================================================
# PHONE MESSAGING SYSTEM
# Chat-style UI inside a phone container with persistent history.
# ============================================================

default _phone_chat_girl = None
default _phone_chat_scroll = 99999.0
default _phone_chat_exit = "back"
# ("close" / "home", time.time()) while a Back / Home press made during a typing pause is still to be honoured
default _phone_leave_pending = None
default _harem_group_id = None

init python:

    # ----------------------------------------------------------
    # Message helpers
    # ----------------------------------------------------------

    def phone_add_msg(girl_gid, sender, text, msg_type="text"):
        """Add a message to chat history.
        sender: "player" or girl_gid
        msg_type: "text", "photo", "system"
        """
        msgs = getattr(store.Player, "phone_messages", None)
        if msgs is None:
            store.Player.phone_messages = {}
            msgs = store.Player.phone_messages
        if girl_gid not in msgs:
            msgs[girl_gid] = []
        msgs[girl_gid].append({
            "sender": sender,
            "text": str(text),
            "day": getattr(store, "Day", 1),
            "time": getattr(store, "TimeIndex", 0),
            "type": msg_type,
        })
        # Her first text TO him puts her number in his phone (author 2026-10-11): a girl whose number
        # he doesn't have yet (Shion's grade texts on her cold step) could text him with no way to
        # answer. She wrote first: he has her number now. Girls only (an NPC chat keys by partner_id),
        # and never a "system" / "typing" row. _number_from_her_text: the flows that want to SAY so
        # (the grade thread's closing note) read it.
        if sender == girl_gid and msg_type in ("text", "photo") and girl_gid in GIRL_BY_ID:
            if not hasattr(store.Player, "phone_contacts"):
                store.Player.phone_contacts = set()
            if girl_gid not in store.Player.phone_contacts:
                store.Player.phone_contacts.add(girl_gid)
                GIRL_BY_ID[girl_gid]._number_from_her_text = True
                print("[PHONE] %s texted him first: her number joined his contacts" % girl_gid)

    def phone_get_msgs(girl_gid):
        """Get chat history list for a girl."""
        msgs = getattr(store.Player, "phone_messages", {})
        return msgs.get(girl_gid, [])

    def phone_msg_time_label(msg):
        """Return readable time from message dict."""
        _names = [_("Morning"), _("Midday"), _("Evening"), _("Night")]
        t = msg.get("time", 0)
        d = msg.get("day", 1)
        tname = _names[t] if 0 <= t < len(_names) else "???"
        return _tl_fmt(_("Day %d, %s"), d, _tl(tname))

    # ----------------------------------------------------------
    # Quick response generator
    # Uses existing dialogue where possible.
    # ----------------------------------------------------------

    _PHONE_CHAT_PLAYER_LINES = [
        _("Hey, what are you up to?"),
        _("Just thinking about you."),
        _("How's your day going?"),
        _("Anything interesting happening?"),
        _("What are you doing right now?"),
    ]

    _PHONE_CHAT_GIRL_RESPONSES = {
        "hardcore_sex": [
            _("Not much. Bored out of my mind."),
            _("Working out. What do you want?"),
            _("Ugh, studying. Kill me."),
            _("Just got back from the gym. I'm sore everywhere."),
            _("Nothing interesting. Entertain me."),
        ],
        "cute_sex": [
            _("Hi! I was just reading a book~"),
            _("Oh! Hey! I'm doing okay, thanks for asking!"),
            _("Just relaxing... it's nice to hear from you."),
            _("I was thinking about you too, actually..."),
            _("Not much! Just a quiet day. How about you?"),
        ],
        "cheater": [
            _("Hey~ My {hint}%(pl)s{/hint} is out, perfect timing."),

            _("Just pretending to be busy. What's up?"),
            _("Texting you behind %(poss)s back, as usual."),
            _("Bored. %(Pp)s's being boring. You're not."),
            _("Nothing. Wish I was doing something more... fun."),
        ],
        "camera_lover": [
            _("Just took some selfies. Wanna see?"),
            _("Practicing poses. For... reasons."),
            _("Hey! I was about to send you something~"),
            _("Scrolling through my photos. I look good today."),
            _("Nothing! Well... maybe taking a few pics."),
        ],
        "loyal": [
            _("Hey. I probably shouldn't be texting you..."),
            _("I'm with my {hint}%(pl)s{/hint}. But... hi."),

            _("Just hanging out. Nothing I should tell you about."),
            _("You know I have a {hint}%(pl)s{/hint}, right? ...But hi."),

            _("Studying. Totally not checking my phone every 5 seconds."),
        ],
        "_default": [
            _("Hey! Not much, just hanging around."),
            _("Just chilling. What's up?"),
            _("Oh hey! I was about to text you actually."),
            _("Nothing exciting. You?"),
            _("Just thinking. What do you need?"),
        ],
    }

    _PHONE_FLIRT_PLAYER_LINES = [
        _("You looked really good today."),
        _("Can't stop thinking about you."),
        _("I wish you were here right now..."),
        _("You're on my mind. A lot."),
        _("Miss you."),
    ]

    _PHONE_FLIRT_GIRL_RESPONSES = {
        "hardcore_sex": [
            _("Yeah? Then come do something about it."),
            _("Sweet talk won't work. Actions speak louder."),
            _("Flattery. I like it. Keep going."),
            _("You better back that up in person."),
            _("Hmm. You're bold over text. I like that."),
        ],
        "cute_sex": [
            _("R-really? That's so sweet..."),
            _("You're making me blush and you're not even here!"),
            _("I... I think about you too. A lot."),
            _("Stop it, you're going to make me smile all day."),
            _("That's... really nice to hear. Thank you."),
        ],
        "cheater": [
            _("More than my {hint}%(pl)s{/hint} does, that's for sure."),

            _("Keep talking like that and I might sneak out tonight."),
            _("You're dangerous. I like it."),
            _("Say that to my face next time. I dare you."),
            _("Careful. I might take you seriously."),
        ],
        "camera_lover": [
            _("Want a photo to remember me by? ;)"),
            _("You charmer. I might send you something special."),
            _("Keep that up and I'll give you a private show."),
            _("Aww~ You know how to make a girl feel wanted."),
            _("Should I send you proof of how good I look right now?"),
        ],
        "_default": [
            _("You're sweet. Thanks for saying that."),
            _("Haha, smooth. I'll give you that one."),
            _("That made me smile. Don't let it go to your head."),
            _("Oh? Tell me more..."),
            _("You always know what to say, huh?"),
        ],
    }

    _PHONE_INVITE_ACCEPT = [
        _("Sure! Give me a few minutes."),
        _("Okay, I'm on my way!"),
        _("I'll be right there~"),
        _("Already heading out the door."),
        _("Yay! Be there soon!"),
    ]

    _PHONE_INVITE_DECLINE = [
        _("I can't right now, sorry."),
        _("Maybe later? I'm busy."),
        _("Not feeling it right now."),
        _("I wish I could, but not today."),
        _("Rain check?"),
    ]

    # ----------------------------------------------------------
    # Phone-mode interceptors
    # When _phone_mode is True, Say_Line/set_scene_expression/set_girl_sprite
    # are skipped so dialogue goes to phone messages, not screen.
    # ----------------------------------------------------------
    store._phone_mode = False
    store._phone_mode_girl = None

    def _phone_mode_on(girl):
        store._phone_mode = True
        store._phone_mode_girl = girl

    def _phone_mode_off():
        store._phone_mode = False
        store._phone_mode_girl = None

    def _phone_girl_response(girl, category):
        """Pick a response line based on girl's primary trait."""
        pool_map = {
            "chat": _PHONE_CHAT_GIRL_RESPONSES,
            "flirt": _PHONE_FLIRT_GIRL_RESPONSES,
        }
        pools = pool_map.get(category, _PHONE_CHAT_GIRL_RESPONSES)
        for t in ("hardcore_sex", "cute_sex", "cheater", "camera_lover", "loyal"):
            if girl.has_trait(t) and t in pools:
                # "cheater" lines reference boyfriend — skip if she's single
                if t == "cheater" and not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
                    continue
                # cheater ("my boyfriend is out, perfect timing"), camera_lover (selfies) and
                # loyal ("I'm with my boyfriend. But... hi.") pools voice the trait; the
                # hardcore/cute pools are tone and reveal nothing
                if t in ("cheater", "camera_lover", "loyal") and hasattr(girl, "discover"):
                    girl.discover("discovered_trait_%s" % t)
                return _format_partner_line(girl, renpy.random.choice(pools[t]))
        return _format_partner_line(girl, renpy.random.choice(pools.get("_default", ["Hey."])))

    def _phone_get_flirt_text(girl, action_key, reaction_mode):
        """Get the flirt response text without showing sprites.
        Same picker as rod_flirt_say (rod_flirt_line), plus a fallback by reaction mode."""
        text = rod_flirt_line(girl, action_key, reaction_mode)
        if not text:
            # Fallback based on reaction mode
            if "no" in reaction_mode:
                text = _("I don't think so.")
            elif "shy" in reaction_mode:
                text = _("T-that's sweet...")
            elif "enthusiastic" in reaction_mode:
                text = _("Heh, you really know what to say~")
            elif "obedient" in reaction_mode:
                text = _("If you say so...")
            else:
                text = _("Haha, thanks.")
        return text

# ============================================================
# PHONE CHAT SCREEN — Messenger style
# ============================================================

init python:

    # SVG-based bubble backgrounds (9-patch scaled, rounded corners baked into SVG)
    _BUBBLE_PLAYER = Frame(
        Transform("images/menus/Chat_Player1.png",
                  matrixcolor=SaturationMatrix(0.0) * TintMatrix("#9333ea")),
        26, 26, 26, 26
    )
    _BUBBLE_GIRL   = Frame("images/menus/Chat_Girl1.png", 26, 26, 26, 26)

    def _chat_build_grouped(girl_gid):
        """Pre-process messages: compute grouping, spacing, corner style per bubble."""
        raw = phone_get_msgs(girl_gid)
        out = []
        prev_sender = None
        prev_day = None
        for i, m in enumerate(raw):
            sender = m.get("sender", "")
            mtype  = m.get("type", "text")
            day_label = phone_msg_time_label(m)
            show_day = (day_label != prev_day)

            # next sender (look-ahead)
            nxt_sender = None
            if i + 1 < len(raw):
                nxt = raw[i + 1]
                if nxt.get("type", "text") not in ("system", "typing"):
                    nxt_sender = nxt.get("sender", "")

            if mtype in ("system", "typing"):
                group_pos = "solo"
                spacing = 12
            else:
                same_prev = (sender == prev_sender) and not show_day
                same_next = (sender == nxt_sender)
                if same_prev and same_next:
                    group_pos = "mid"
                elif same_prev:
                    group_pos = "last"
                elif same_next:
                    group_pos = "first"
                else:
                    group_pos = "solo"
                spacing = 4 if same_prev else 12

            out.append({
                "sender": sender,
                "text": _safe_phone_text(m.get("text", "")),
                "type": mtype,
                "day_label": day_label,
                "show_day": show_day,
                "group": group_pos,   # solo / first / mid / last
                "spacing": spacing,
            })
            if mtype not in ("system", "typing"):
                prev_sender = sender
            prev_day = day_label
        return out

    # ----------------------------------------------------------
    # GROUP CHAT helpers
    # ----------------------------------------------------------

    def _phone_finalize_group(sel_gids):
        """Create a group from the selected gids, add system msg, trigger reactions,
        then open the group chat. Called from screen action."""
        gid_list = list(sel_gids)[:3]
        names = [_girl_name_by_gid(g) for g in gid_list]
        group_name = " & ".join(names[:3])
        if len(names) > 3:
            group_name += " +%d" % (len(names) - 3)
        new_gid = phone_create_group(group_name, gid_list)
        phone_group_add_msg(new_gid, "player", _tl(_("Group created!")), "system")
        unlock_achievement("group_chat")
        _group_creation_reactions(new_gid, gid_list)
        # Find the group dict and open chat via label
        new_group = None
        for pg in phone_get_groups():
            if pg["id"] == new_gid:
                new_group = pg
                break
        if new_group is not None:
            store._pending_new_group = new_group
            store._phone_girls_arrived = []
            renpy.call_in_new_context("_phone_open_new_group")
            # Restore sprites for girls who arrived during the group chat
            _arrived = getattr(store, "_phone_girls_arrived", [])
            for _agid in _arrived:
                _ag = GIRL_BY_ID.get(_agid)
                if _ag and getattr(_ag, "loc", None) == store.CurrentLocation:
                    _asl = getattr(_ag, "SpriteLoc", StageCenter)
                    if _asl == StageLeft:
                        _atf = slot_left
                    elif _asl == StageRight:
                        _atf = slot_right
                    else:
                        _atf = slot_center
                    set_girl_sprite(_ag.gid, pose="standing", at_list=[_atf])
            _any_new_arrived = len(_arrived) > 0
            store._phone_girls_arrived = []
            if _any_new_arrived:
                _phone_restore_others()
                _loc = store.CurrentLocation
                _jump_to = _LOC_LOOPS.get(_loc)   # central map (navigation.rpy); the local copy had no "tenny_room"
                print("[PHONE_GROUP] new group arrived=%s loc=%s jump=%s" % ([g for g in _arrived], _loc, _jump_to))
                if _jump_to:
                    renpy.jump(_jump_to)
        # Phone is still open — restore the flag (new context set it to False)
        store._phone_is_open = True
        # Go back to contacts
        renpy.show_screen("phone_contacts_screen")

    def phone_create_group(name, girl_gids):
        """Create a new group chat. girl_gids = list of gid strings."""
        groups = getattr(store.Player, "phone_groups", None)
        if groups is None:
            store.Player.phone_groups = []
            groups = store.Player.phone_groups
        # First free id: groups get deleted (dissolve, harem, new partner), so len + 1 can land on a live id
        # or on the leftover messages of a deleted group.
        _taken = set(g.get("id") for g in groups) | set(getattr(store.Player, "phone_group_messages", None) or {})
        _n = len(groups) + 1
        while ("grp_%d" % _n) in _taken:
            _n += 1
        group_id = "grp_%d" % _n
        groups.append({
            "id": group_id,
            "name": str(name),
            "members": list(girl_gids),
        })
        return group_id

    def phone_get_groups():
        """Return list of all groups."""
        return getattr(store.Player, "phone_groups", [])

    def phone_group_delete(group_id):
        """Remove a group and its chat history for good: the player tidying duplicate groups (tester
        2026-10-10). The harem group never offers it (the harem system owns that one)."""
        _groups = getattr(store.Player, "phone_groups", []) or []
        store.Player.phone_groups = [g for g in _groups if g.get("id") != group_id]
        _gmsgs = getattr(store.Player, "phone_group_messages", None)
        if _gmsgs:
            _gmsgs.pop(group_id, None)
        print("[PHONE] group %s deleted (%d groups left)" % (group_id, len(store.Player.phone_groups)))

    # ── Group creation: girl+girl OR girl + HER OWN partner NPC ──────────
    def _group_create_candidates():
        """Ordered candidates for the create-group screen: each girl, then her
        partner NPC.  The screen handles the 'no number' gray-out."""
        out = []
        for g in store.ALL_GIRLS:
            out.append(g)
            if g.has_npc_partner():
                npc = get_npc_partner_for(g)
                if npc:
                    out.append(npc)
        return out

    def _group_cand_allowed(cand_gid, selected):
        """Gray-out rule for group creation (max 3 members, max 1 NPC).
        NPC requires his GF already selected. Can't deselect GF while her
        NPC is selected. Returns True if cand_gid can be (de)selected."""
        sel = list(selected)
        c_is_npc = str(cand_gid).startswith("npc_")
        if cand_gid in sel:
            if not c_is_npc:
                for s in sel:
                    if str(s).startswith("npc_"):
                        _p = NPC_PARTNERS.get(s)
                        if _p and _p.girl_gid == cand_gid:
                            return False     # can't deselect GF while her NPC is selected
            return True
        if len(sel) >= 3:
            return False
        if len(sel) == 0:
            return True
        if c_is_npc:
            if any(str(s).startswith("npc_") for s in sel):
                return False                 # max 1 NPC per group
            _p = NPC_PARTNERS.get(cand_gid)
            return bool(_p) and _p.girl_gid in sel
        # Girl candidate: if an NPC is selected without his GF, only allow his GF
        for s in sel:
            if str(s).startswith("npc_"):
                _p = NPC_PARTNERS.get(s)
                if _p and _p.girl_gid not in sel:
                    return cand_gid == _p.girl_gid
        return True

    def _group_has_partner(group):
        """True if the group is a girl + her partner NPC (has an npc_ member)."""
        return any(str(m).startswith("npc_") for m in group.get("members", []))

    def _group_partner_and_girl(group):
        """For a girl+partner group, return (npc, girl); else fills what it can."""
        _npc = None
        _girl = None
        for m in group.get("members", []):
            if str(m).startswith("npc_"):
                _npc = NPC_PARTNERS.get(m)
            else:
                _girl = GIRL_BY_ID.get(m)
        return (_npc, _girl)

    # ----------------------------------------------------------
    # Harem group helpers
    # ----------------------------------------------------------

    def _is_harem_group(group):
        _hgid = getattr(store, "_harem_group_id", None)
        return _hgid is not None and group.get("id") == _hgid

    def _harem_away_members(group=None):
        """Members of the harem group who are away (giving birth). ONE rule for every harem flow while this
        is not empty: nothing is decided without her. No vote runs, no pending flag is consumed."""
        _grp = group if group is not None else _get_harem_group()
        return [GIRL_BY_ID[_gid] for _gid in (_grp or {}).get("members", [])
                if _gid in GIRL_BY_ID and girl_is_away(GIRL_BY_ID[_gid])]

    def _get_harem_group():
        _hgid = getattr(store, "_harem_group_id", None)
        if _hgid is None:
            return None
        for g in phone_get_groups():
            if g["id"] == _hgid:
                return g
        return None

    def _create_harem_group(first_girl):
        gid = phone_create_group(_("My Girls"), [first_girl.gid])
        store._harem_group_id = gid
        print("[HAREM_GROUP] Created harem group %s with %s" % (gid, first_girl.gid))
        return gid

    def _harem_propose_candidates():
        hg = _get_harem_group()
        if not hg:
            return []
        members = set(hg["members"])
        contacts = getattr(store.Player, "phone_contacts", set())
        return [g for g in store.ALL_GIRLS if g.gid not in members and g.gid in contacts]

    def phone_group_add_msg(group_id, sender, text, msg_type="text"):
        """Add message to group chat. sender = 'player' or girl gid."""
        msgs = getattr(store.Player, "phone_group_messages", None)
        if msgs is None:
            store.Player.phone_group_messages = {}
            msgs = store.Player.phone_group_messages
        if group_id not in msgs:
            msgs[group_id] = []
        msgs[group_id].append({
            "sender": sender,
            "text": str(text),
            "day": getattr(store, "Day", 1),
            "time": getattr(store, "TimeIndex", 0),
            "type": msg_type,
        })

    def phone_group_get_msgs(group_id):
        """Get message list for a group."""
        msgs = getattr(store.Player, "phone_group_messages", {})
        return msgs.get(group_id, [])

    def _safe_phone_text(txt):
        """Escape [ in phone messages so Ren'Py text doesn't eval them.
        Resolves [Player.Name] first (legitimate substitution), then
        flattens all remaining brackets."""
        if not txt:
            return ""
        if "[Player.Name]" in txt:
            txt = txt.replace("[Player.Name]", store.Player.Name)
        return txt.replace("[[", "[").replace("[", "[[")

    def _group_chat_build_grouped(group_id):
        """Build grouped messages for group chat display."""
        raw = phone_group_get_msgs(group_id)
        out = []
        prev_sender = None
        prev_day = None
        for i, m in enumerate(raw):
            sender = m.get("sender", "")
            mtype  = m.get("type", "text")
            day_label = phone_msg_time_label(m)
            show_day = (day_label != prev_day)

            nxt_sender = None
            if i + 1 < len(raw):
                nxt = raw[i + 1]
                if nxt.get("type", "text") not in ("system", "typing"):
                    nxt_sender = nxt.get("sender", "")

            if mtype in ("system", "typing"):
                group_pos = "solo"
                spacing = 12
            else:
                same_prev = (sender == prev_sender) and not show_day
                same_next = (sender == nxt_sender)
                if same_prev and same_next:
                    group_pos = "mid"
                elif same_prev:
                    group_pos = "last"
                elif same_next:
                    group_pos = "first"
                else:
                    group_pos = "solo"
                spacing = 4 if same_prev else 12

            out.append({
                "sender": sender,
                "text": _safe_phone_text(m.get("text", "")),
                "type": mtype,
                "day_label": day_label,
                "show_day": show_day,
                "group": group_pos,
                "spacing": spacing,
            })
            if mtype not in ("system", "typing"):
                prev_sender = sender
            prev_day = day_label
        return out

    def _girl_name_by_gid(gid):
        """Get Name from gid (girl or NPC partner)."""
        for g in store.ALL_GIRLS:
            if g.gid == gid:
                return g.Name
        npc = NPC_PARTNERS.get(gid)
        if npc is None and str(gid).startswith("npc_"):
            # NPC_PARTNERS is a lazily-rebuilt runtime dict (empty after load until
            # get_npc_partner_for runs), so a direct .get can miss. Resolve via the
            # owning girl (that call rebuilds if needed) so we never show the raw id.
            for g in store.ALL_GIRLS:
                if getattr(g, "npc_partner_id", None) == gid and g.has_npc_partner():
                    npc = get_npc_partner_for(g)
                    break
        if npc:
            return npc.Name
        return gid.capitalize()

    def _npc_partner_label(npc_gid):
        npc = NPC_PARTNERS.get(npc_gid)
        if not npc:
            return _tr("(partner)")
        girl = GIRL_BY_ID.get(npc.girl_gid)
        if not girl:
            return _tr("(partner)")
        if npc.gender == "female":
            return "(" + _tr("%s's GF") % girl.Name + ")"
        return "(" + _tr("%s's BF") % girl.Name + ")"

    _GIRL_AVATAR_MAP = {
        "gwen": "images/characters/Gwen/Gwen Avatar.png",
        "rogue": "images/characters/Rogue/Rogue Avatar.png",
        "ntw": "images/characters/Negasonic/Ntw Avatar.png",
        "tenny": "images/characters/Tenny/Tenny Avatar.png",
        "shion": "images/characters/Shion/Shion Avatar.png",
    }

    def _girl_avatar_by_gid(gid):
        """Get avatar path from gid (girl or NPC partner). Falls back to Char_Default.png for missing art."""
        if gid.startswith("npc_"):
            return "images/menus/Char_Default.png"
        _path = _GIRL_AVATAR_MAP.get(gid, "images/menus/Char_%s.png" % gid.capitalize())
        return _path if renpy.loadable(_path) else "images/menus/Char_Default.png"

    # Bubble colors per girl for group chat
    _GROUP_BUBBLE_COLORS = {
        "gwen":  "#ff6b9d",
        "rogue": "#9b59b6",
        "ntw":   "#00d4aa",
        "tenny": "#7ecb8f",
    }

    # ----------------------------------------------------------
    # GROUP CREATION REACTIONS
    # ----------------------------------------------------------

    def _group_creation_reactions(group_id, member_gids):
        """
        Generate initial messages from each girl when added to a group.
        Reactions depend on:
        - How much each girl likes the others (Girl_like / gf_like_tier)
        - Whether girls are dating the player or each other
        - Traits (loyal, polyamorous, cheater)
        - Whether they're in each other's harem_accepted
        """
        girls_in = []
        for gid in member_gids:
            for g in store.ALL_GIRLS:
                if g.gid == gid:
                    girls_in.append(g)
                    break

        for girl in girls_in:
            other_girls = [g for g in girls_in if g.gid != girl.gid]
            if not other_girls:
                continue
            if girl_is_away(girl):
                continue   # she can be added to a group, she just does not answer from her parents' place

            # Gather relationship context
            girl_love = getattr(girl, "Love", 0)
            girl_dating_player = girl.is_dating_player() if hasattr(girl, "is_dating_player") else False
            girl_traits = getattr(girl, "traits", set()) or set()
            is_poly = "polyamorous" in girl_traits
            is_loyal = "loyal" in girl_traits
            is_cheater = "cheater" in girl_traits
            harem = getattr(girl, "harem_accepted", set()) or set()

            # Check relationship with each other girl
            worst_tier = "close"
            best_tier = "hostile"
            has_hostile = False
            has_close = False
            has_rival = False  # another girl also dating player
            has_girl_partner = False  # dating another girl in group
            all_accepted = True  # all others in harem_accepted

            tier_order = {"hostile": 0, "distant": 1, "friendly": 2, "close": 3}

            for other in other_girls:
                tier = girl.gf_like_tier(other.gid)
                tier_val = tier_order.get(tier, 1)

                if tier_val < tier_order.get(worst_tier, 3):
                    worst_tier = tier
                if tier_val > tier_order.get(best_tier, 0):
                    best_tier = tier

                if tier == "hostile":
                    has_hostile = True
                if tier == "close":
                    has_close = True

                # Check if other is also dating player
                other_dating = other.is_dating_player() if hasattr(other, "is_dating_player") else False
                if girl_dating_player and other_dating:
                    has_rival = True

                # Check if they're girl partners
                if getattr(girl, "girl_partner_id", None) == other.gid:
                    has_girl_partner = True

                # Check harem acceptance
                if other.gid not in harem:
                    all_accepted = False

            # Pick reaction based on context
            msgs = []

            # --- HOSTILE to someone in group ---
            if has_hostile:
                hostile_names = [o.Name for o in other_girls if girl.gf_like_tier(o.gid) == "hostile"]
                h_name = hostile_names[0] if hostile_names else "someone"
                options = [
                    _tl_fmt(_("Why is %s here?"), h_name),
                    _tl_fmt(_("Seriously? You added %s?"), h_name),
                    _tl_fmt(_("I'd rather not be in a group with %s..."), h_name),
                    _tl_fmt(_("Ugh. %s? Really?"), h_name),
                    _tl_fmt(_("This better be worth it. I can't stand %s."), h_name),
                ]
                msgs.append(renpy.random.choice(options))

                # Extra snark if loyal and rival
                if has_rival and is_loyal:
                    msgs.append(_("And I know what you're doing, putting us together like this."))

            # --- RIVAL (both dating player, no hostility) ---
            elif has_rival and not has_hostile:
                if all_accepted or is_poly:
                    options = [
                        _("Haha, the whole family in one group?"),
                        _("This should be fun~ All of us together."),
                        _("Oooh a group chat with everyone? I love it."),
                        _("Finally! We should've done this sooner."),
                    ]
                    msgs.append(renpy.random.choice(options))
                elif is_loyal:
                    rival_names = [o.Name for o in other_girls
                                   if getattr(o, "Love", 0) >= 700
                                   and ("sex" in getattr(o, "intimacy_flags", set()) or set())]
                    r_name = rival_names[0] if rival_names else "her"
                    options = [
                        _tl_fmt(_("Hmm... why did you add %s?"), r_name),
                        _tl_fmt(_("Is there something going on between you and %s?"), r_name),
                        _tl_fmt(_("I don't mind a group, but... %s too?"), r_name),
                        _("Interesting choice of members..."),
                    ]
                    msgs.append(renpy.random.choice(options))
                elif is_cheater:
                    options = [
                        _("Oh, this is going to be interesting~"),
                        _("All your girls in one chat? Bold move."),
                        _("Hehe, does she know about us?"),
                    ]
                    msgs.append(renpy.random.choice(options))
                else:
                    options = [
                        _("Oh, a group? Sure, I guess."),
                        _("This is... unexpected."),
                        _("All of us? Okay then."),
                    ]
                    msgs.append(renpy.random.choice(options))

            # --- GIRL PARTNER in group ---
            elif has_girl_partner:
                partner_name = ""
                for o in other_girls:
                    if getattr(girl, "girl_partner_id", None) == o.gid:
                        partner_name = o.Name
                        break
                options = [
                    _tl_fmt(_("Aww, me and %s in a group together!"), partner_name),
                    _tl_fmt(_("Yay! %s is here too!"), partner_name),
                    _tl_fmt(_("This is nice~ Hi %s!"), partner_name),
                    _("A group with my favorite person? Yes please!"),
                ]
                msgs.append(renpy.random.choice(options))

            # --- CLOSE friends ---
            elif has_close:
                close_names = [o.Name for o in other_girls if girl.gf_like_tier(o.gid) == "close"]
                c_name = close_names[0] if close_names else "everyone"
                options = [
                    _tl_fmt(_("Oh nice! Hey %s!"), c_name),
                    _tl_fmt(_("A group with %s? Love it!"), c_name),
                    _("This is going to be so much fun!"),
                    _("Omg yes! I love group chats!"),
                    _("Hey everyone! What's this about?"),
                    _("Hiiii! What are we planning?"),
                ]
                msgs.append(renpy.random.choice(options))

            # --- FRIENDLY (neutral positive) ---
            elif best_tier == "friendly":
                options = [
                    _("Hey! What's this group for?"),
                    _("Oh, a group chat? Cool!"),
                    _("Hi everyone."),
                    _("What's up? Why the group?"),
                    _("Sure, I'm in. What's the occasion?"),
                    _("Heyyy, what's going on?"),
                ]
                msgs.append(renpy.random.choice(options))

            # --- DISTANT (barely know each other) ---
            elif best_tier == "distant":
                options = [
                    _("Um, hi?"),
                    _("Oh. A group."),
                    _("Hey..."),
                    _("What's this about?"),
                    _("Hi. Do we... need a group?"),
                    _("Okay... hi everyone I guess."),
                ]
                msgs.append(renpy.random.choice(options))

            # --- Fallback ---
            else:
                msgs.append(_("Hi."))

            # Send all messages
            for msg in msgs:
                phone_group_add_msg(group_id, girl.gid, msg)

        _store_group_tiers(group_id, member_gids)

    # ----------------------------------------------------------
    # GROUP FRIENDSHIP UPDATES
    # ----------------------------------------------------------

    _GROUP_TIER_CHANGE_MSGS = {
        ("hostile", "distant"): [
            _("Hmm... maybe %s isn't as bad as I thought."),
            _("I guess %s is... okay."),
            _("Fine, %s isn't the worst."),
            _("%s has been less annoying lately."),
        ],
        ("hostile", "friendly"): [
            _("You know what, %s is actually pretty cool."),
            _("I take back what I said about %s. She's alright."),
            _("Okay, I'll admit it. %s is nice."),
        ],
        ("hostile", "close"): [
            _("I can't believe I'm saying this, but %s is amazing!"),
            _("Funny how things change... %s is one of my favorite people now."),
        ],
        ("distant", "friendly"): [
            _("%s is actually fun to talk to!"),
            _("I've been getting along with %s lately."),
            _("%s is growing on me, not gonna lie."),
        ],
        ("distant", "close"): [
            _("%s is seriously the best!"),
            _("I love hanging out with %s!"),
        ],
        ("friendly", "close"): [
            _("%s is honestly one of my favorite people!"),
            _("I love %s so much, she's the best!"),
            _("%s is amazing, I'm so glad we're friends!"),
        ],
        ("close", "friendly"): [
            _("%s has been kind of distant lately..."),
            _("Things feel different with %s."),
            _("I don't know what's up with %s..."),
        ],
        ("close", "distant"): [
            _("I don't think %s likes me very much anymore."),
            _("%s barely talks to me now..."),
            _("What happened with %s? We used to be so close."),
        ],
        ("close", "hostile"): [
            _("I'm done with %s. Seriously."),
            _("%s can forget about being friends."),
        ],
        ("friendly", "distant"): [
            _("%s has been cold to me lately."),
            _("I don't really click with %s anymore."),
            _("%s and I just don't vibe anymore."),
        ],
        ("friendly", "hostile"): [
            _("I can't stand %s anymore."),
            _("Done pretending to like %s."),
            _("%s really gets on my nerves now."),
        ],
        ("distant", "hostile"): [
            _("%s is so annoying, I can't deal."),
            _("Why is %s even in this group?"),
            _("I really don't like %s."),
        ],
    }

    def _store_group_tiers(group_id, member_gids):
        """Store current friendship tiers for all girl pairs in a group."""
        tiers = getattr(store.Player, "_group_friendship_tiers", None)
        if tiers is None:
            store.Player._group_friendship_tiers = {}
            tiers = store.Player._group_friendship_tiers
        group_tiers = {}
        for gid in member_gids:
            girl = GIRL_BY_ID.get(gid)
            if not girl:
                continue
            for other_gid in member_gids:
                if other_gid == gid:
                    continue
                key = "%s:%s" % (gid, other_gid)
                group_tiers[key] = girl.gf_like_tier(other_gid)
        tiers[group_id] = group_tiers

    def _check_group_friendship_updates(group_id, member_gids):
        """Compare current friendship tiers against stored ones.
        If a tier changed, inject new messages and update storage."""
        tiers_dict = getattr(store.Player, "_group_friendship_tiers", {})
        old_tiers = tiers_dict.get(group_id)

        if old_tiers is None:
            _store_group_tiers(group_id, member_gids)
            return

        for gid in member_gids:
            girl = GIRL_BY_ID.get(gid)
            if not girl:
                continue
            for other_gid in member_gids:
                if other_gid == gid:
                    continue
                key = "%s:%s" % (gid, other_gid)
                current_tier = girl.gf_like_tier(other_gid)
                old_tier = old_tiers.get(key)

                if old_tier and current_tier != old_tier:
                    other = GIRL_BY_ID.get(other_gid)
                    if not other:
                        continue
                    pool = _GROUP_TIER_CHANGE_MSGS.get((old_tier, current_tier), [])
                    if pool and not girl_is_away(girl):   # away: the tier is stored, she posts nothing
                        msg = _tl_fmt(renpy.random.choice(pool), other.Name)
                        phone_group_add_msg(group_id, gid, msg)
                        print("[GroupChat] %s -> %s friendship: %s -> %s" % (gid, other_gid, old_tier, current_tier))

        _store_group_tiers(group_id, member_gids)

    def _group_bubble_for(gid):
        """Return a tinted bubble Frame for a girl in group chat."""
        color = _GROUP_BUBBLE_COLORS.get(gid, "#3498db")
        return Frame(
            Transform("images/menus/Chat_Girl1.png",
                      matrixcolor=SaturationMatrix(0.0) * TintMatrix(color)),
            26, 26, 26, 26
        )

    # ----------------------------------------------------------
    # DICK PIC PROGRESSIVE REACTIONS (3 tiers by send count)
    # ----------------------------------------------------------
    # Tier 1: 1-2 sends (shocked/surprised)
    # Tier 2: 3-5 sends (getting used to it)
    # Tier 3: 6+  sends (accustomed/casual)

    _DP_REACTIONS = {
        "accepted": {
            1: {
                "lesbian_cute": [_("W-why would you send me that?! I'm a lesbian! ...Delete this conversation."), _("Oh my god... I did NOT need to see that... why is my face so hot right now...?"), _("I hate you. I hate that you sent this. I hate that I'm still looking at it.")],
                "lesbian_hc": [_("A dick pic. Really? ...At least it's not small."), _("You think a picture of your dick will impress a lesbian? ...It's not the worst I've seen."), _("Bold move for a man sending this to a woman who doesn't like men. ...Whatever.")],
                "lesbian": [_("Why did you send me this...? I'm a lesbian... I don't want to see... okay I saw it."), _("I should be disgusted. I AM disgusted. ...Why am I zooming in?"), _("A man's... on my phone... this is wrong on so many levels. ...Don't send another one. (Maybe.)")],
                "camera": [_("Ooh~ Not bad! Now I want to see it in person."), _("Nice angle! You should let me take some photos of it next time ;)"), _("Well well well... someone's feeling confident. I like it.")],
                "cum_slut": [_("You're making me hungry... when can I have the real thing?"), _("That's a LOT... I want every drop.")],
                # added to "cum_slut" once she has had it in her mouth (she knows the taste)
                "cum_slut_tasted": [_("Mmm... I can almost taste it through the screen...")],
                "hardcore": [_("Is that supposed to impress me? ...It does. A little."), _("Bold. I'll give you that. Now come show me in person."), _("Not bad. But photos don't count. Use it on me or don't bother.")],
                "cute": [_("Oh my god! You can't just SEND that! ...It's... um... okay I looked."), _("W-what is this?! I... oh... oh my..."), _("Delete this! What if someone sees my phone?! ...But also... wow.")],
                "seen": [_("I've seen it in person and it's STILL surprising in a photo..."), _("You're so shameless... but I'm not complaining."), _("I remember that... now I want to see it again for real.")],
                "default": [_("I can't believe you just sent me that... it's... not bad though."), _("Oh! That's... unexpected. And... larger than I expected."), _("You're crazy for sending this! ...But I'm saving it.")],
            },
            2: {
                "lesbian_cute": [_("Not this again... you know I'm a lesbian, right? ...Fine, I looked."), _("Another one? Really? ...Okay, it's not THAT bad. But still."), _("You're persistent, I'll give you that... stop making me look at these.")],
                "lesbian_hc": [_("Again? I know what it looks like by now. ...It's fine, I guess."), _("You really don't give up, do you? ...At least the lighting is better this time."), _("Another one. I'm starting to think you enjoy being rejected by a lesbian.")],
                "lesbian": [_("Oh, another one. I'm... less surprised this time. That worries me."), _("You again with the... yeah, I know what it is. I'm not zooming in this time. (Okay, maybe a little.)"), _("At this point I've seen it enough times to... no, I'm still a lesbian. But thanks?")],
                "camera": [_("Another angle? Nice, you're getting better at this."), _("You know I have a whole folder of these now, right?"), _("Keep them coming~ I'm building a collection.")],
                "cum_slut": [_("Mmm, you know exactly what this does to me..."), _("Another one? You're teasing me... when are you going to deliver in person?"), _("I swear these photos make me hungrier each time...")],
                "hardcore": [_("Still sending these? At least you're consistent."), _("You again. ...Fine, it's still impressive. Happy?"), _("Another one? You better be planning to back this up in person soon.")],
                "cute": [_("Oh god, not again... I mean... okay, I'll admit I look every time now."), _("You sent another one?! ...I kind of expected it this time though..."), _("I should be used to these by now... I'm still blushing though.")],
                "seen": [_("I know what it looks like in person AND in photos now... and I still look."), _("You keep sending these like I don't remember... I do. All of them."), _("Is this your daily greeting now? ...I don't hate it.")],
                "default": [_("Another one, huh? I'm starting to recognize it from different angles."), _("You know, at first I was shocked. Now I just... look."), _("Getting bolder with these, aren't you? ...I'm not deleting them.")],
            },
            3: {
                "lesbian_cute": [_("...You know what, just send it. I know what's coming. It's fine."), _("At this point I just open these automatically. Don't tell anyone."), _("I'm a lesbian who regularly looks at dick pics. This is my life now.")],
                "lesbian_hc": [_("I don't even flinch anymore. That probably says something about both of us."), _("Show me something new at least. I've memorized every angle."), _("This is just our thing now, isn't it? The lesbian and her dick pic guy.")],
                "lesbian": [_("Just another day, getting a dick pic from my... whatever you are."), _("I don't even pretend to be disgusted anymore. My sexuality is confused enough."), _("Send. Look. Save. I have a routine now. What have you done to me?")],
                "camera": [_("Ooh, new lighting? You're taking my feedback seriously~"), _("At this point we should do a proper photoshoot. I'll bring my camera."), _("My personal collection keeps growing. Keep them coming!")],
                "cum_slut": [_("You know I look at these every night, right? Send more."), _("I'm addicted to these at this point. Don't you dare stop."), _("Every time I see that notification I get wet. You've trained me.")],
                "hardcore": [_("Good morning to you too. Now come use it."), _("I expect these now. You'd better not stop."), _("Same cock, still impressive. When's the live show?")],
                "cute": [_("Okay, I'll admit it... I look forward to these now."), _("You know what? I don't even blush anymore. ...Okay, a little."), _("I've seen this so many times that I... might miss it if you stopped.")],
                "seen": [_("At this point I could draw it from memory. Still nice though."), _("You and me both know I'm opening this immediately. No shame anymore."), _("I know it by heart but I still smile when I see the notification.")],
                "default": [_("Good morning. Nice pic. Same time tomorrow?"), _("I don't even flinch anymore. Is that bad? ...It's probably bad."), _("You know I save all of these, right? I have quite the collection now.")],
            },
        },
        "rejected": {
            1: {
                "lesbian": [_("What the FUCK?! I'm a LESBIAN! Why would you send me a dick pic?! GROSS!"), _("DELETE THIS. I don't EVER want to see a man's... ANYTHING. EVER. Don't text me again today."), _("Are you INSANE?! I'm a lesbian! That is the most disgusting thing I've ever received!")],
                "cute": [_("WHAT IS THAT?! Why would you send me this?! I barely know you!"), _("Oh my god oh my god oh my god... NO! Delete this! I'm blocking you!"), _("I can't believe you just did that... I feel violated... don't talk to me.")],
                "hardcore": [_("Did I ask for this? No. Send unsolicited pics again and I'll make your life hell."), _("Wow, a dick pic from a guy I barely know. How original. How pathetic."), _("You think your dick is impressive enough to send uninvited? It's not.")],
                "default": [_("What the hell?! I didn't ask for that! Gross!"), _("Are you serious right now?! Delete this conversation and don't talk to me today."), _("You really just sent me a dick pic... wow. Just wow. Stay away from me.")],
            },
            2: {
                "lesbian": [_("Seriously? Again? I've told you I don't want to see this. ...Stop."), _("How many times do I have to tell you? Lesbian. Not interested. Ugh."), _("You're so persistent with these... it's annoying, not flattering.")],
                "cute": [_("Not again... you know how this makes me feel. Please stop."), _("Why do you keep doing this? I've asked you to stop..."), _("Another one... I really wish you'd stop sending these.")],
                "hardcore": [_("Still at it? You'd think the rejections would teach you something."), _("Another day, another unsolicited dick pic. You're predictable."), _("Haven't I made it clear enough? No means no.")],
                "default": [_("Again? Really? You never learn."), _("I'm running out of ways to say 'stop sending me these.'"), _("Another one... at this point I'm just disappointed.")],
            },
            3: {
                "lesbian": [_("Oh look, another one. Whatever. I'm deleting it."), _("*sigh* ...It's just a penis. I'm not even mad anymore. Just bored."), _("You do know this isn't working, right? But fine, keep wasting your time.")],
                "cute": [_("...I don't even react anymore. Are you happy now?"), _("Another one. At this point I just swipe past it."), _("You've sent so many that they don't even shock me anymore. Congratulations?")],
                "hardcore": [_("Yawn. Same picture, same rejection. Save us both the time."), _("Are you going to do this forever? Because I can ignore these forever."), _("I see you sent another. I genuinely don't care anymore.")],
                "default": [_("Oh, it's another one. Must be that time of day."), _("I don't even open these anymore. Auto-delete."), _("Still? ...Fine, whatever. I'm not even going to react.")],
            },
        },
    }

    def _dp_process_dickpic(girl):
        """Process dick pic for one girl. Returns reaction dict or None if on cooldown (or away: she is at
        her parents' giving birth and does not answer, same as no reply)."""
        if girl_is_away(girl):
            print("[DickPic] %s is away: no reply" % girl.gid)
            return None
        cooldown_day = getattr(girl, "_dick_pic_last_day", None)
        if cooldown_day is not None and (store.Day - cooldown_day) < 1:
            return None

        girl._dick_pic_last_day = store.Day
        count = getattr(girl, "_dick_pics_received", 0) + 1
        girl._dick_pics_received = count
        print("[DickPic] %s: send #%d" % (girl.gid, count))

        obed = getattr(girl, "Obed", 0)
        love = getattr(girl, "Love", 0)
        is_les = girl.has_trait("lesbian")
        is_cute = girl.has_trait("cute_sex")
        is_hc = girl.has_trait("hardcore_sex")
        is_cam = girl.has_trait("camera_lover")
        is_exh = girl.has_trait("exhibitionist")
        is_cum = girl.has_trait("cum_slut")
        has_seen = "girl_saw_penis" in (getattr(girl, "intimacy_flags", set()) or set())
        # acts only: positions are preferences, a cowgirl scene would count twice
        total_acts = sum(_v for _k, _v in getattr(girl, "Sex_acts", {}).items() if _k not in _SEX_POSITION_KEYS)

        # The approval engine, like every acceptance (lewd "dick_pic": Love AND Obed, her Control trait through
        # ORDER_CONTROL, her traits and mood). A flat "Obed 200 or Love 500" let a girl at Love 0 enjoy it after one
        # day of spanking (tester 2026-10-11). A lesbian keeps the harder bar she had (Obed-only, +200 of it).
        # Remote: she reads it on her phone, the people around HIM are not around her.
        _dp_cfg = ApprovalRuleFor(girl=girl, action="dick_pic", category="lewd")
        if is_les:
            _dp_cfg["Type"] = "OI"
            _dp_cfg["Bonus"] = _dp_cfg.get("Bonus", 0) - 200
        _dp_dec = ApprovalCheck(girl=girl, T=_dp_cfg["T"], Type=_dp_cfg["Type"], Spread=_dp_cfg["Spread"],
                                Bonus=_dp_cfg["Bonus"], Variation=_dp_cfg["Variation"], ReturnData=True,
                                Action="dick_pic", Location=girl_home_loc(girl), Remote=True)
        accepted = bool(_dp_dec.get("accepted")) or total_acts >= SEX_HISTORY_THRESHOLDS["dickpic_accept_acts"]
        print("[DickPic] %s: approval score=%s T=%s type=%s accepted=%s (acts=%d) -> %s" % (
            girl.gid, _dp_dec.get("score"), _dp_cfg["T"], _dp_cfg["Type"], _dp_dec.get("accepted"), total_acts, accepted))

        tier = 1 if count <= 2 else (2 if count <= 5 else 3)

        disc_trait = None

        if accepted:
            Change_Status(girl, "Obed", 8)
            Change_Status(girl, "Lust", 5, max_val=100)

            if is_les:
                disc_trait = "lesbian"
                key = "lesbian_cute" if is_cute else ("lesbian_hc" if is_hc else "lesbian")
            elif is_cam or is_exh:
                key = "camera"
                # the camera pool voices cameras, not being seen: never an exhibitionist reveal
                disc_trait = "camera_lover" if is_cam else None
            elif is_cum:
                key = "cum_slut"
                disc_trait = "cum_slut"
            elif is_hc:
                key = "hardcore"
                disc_trait = "hardcore_sex"
            elif is_cute:
                key = "cute"
                disc_trait = "cute_sex"
            elif has_seen:
                key = "seen"
            else:
                key = "default"

            pool = _DP_REACTIONS["accepted"][tier].get(key, _DP_REACTIONS["accepted"][tier]["default"])
            if key == "cum_slut" and (getattr(girl, "CumLog", None) or {}).get("mouth", 0) > 0:
                pool = pool + _DP_REACTIONS["accepted"][tier].get("cum_slut_tasted", [])
        else:
            if tier <= 1:
                Change_Status(girl, "Love", -10)
            elif tier == 2:
                Change_Status(girl, "Love", -5)
            else:
                Change_Status(girl, "Love", -3)
            Change_Status(girl, "Obed", 3)

            if is_les:
                key = "lesbian"
                disc_trait = "lesbian"
            elif is_cute:
                # rejection lines don't reveal preference traits
                key = "cute"
            elif is_hc:
                key = "hardcore"
            else:
                key = "default"

            pool = _DP_REACTIONS["rejected"][tier].get(key, _DP_REACTIONS["rejected"][tier]["default"])

            if tier < 3:
                girl.set_temp_status("angry", 1, reason="dick_pic")

        if disc_trait:
            girl.discover("discovered_trait_%s" % disc_trait)

        line = _tl(renpy.random.choice(pool))
        return {"accepted": accepted, "line": line}

style phone_msg_player is text:
    font "fonts/WorkSans-SemiBold.ttf"
    size 20
    color "#ffffff"
    line_spacing 4
    outlines []

style phone_msg_girl is text:
    font "fonts/WorkSans-SemiBold.ttf"
    size 20
    color "#111111"
    line_spacing 4
    outlines []

style phone_msg_day_chip is frame:
    padding (12, 4, 12, 4)
    background Frame("#1e3a4a", 14, 14, 14, 14)

style phone_chat_action_btn is button:
    ysize 46

style phone_chat_vscrollbar is vscrollbar:
    xsize 24
    base_bar Solid("#1a2730")
    thumb Solid("#00e5ff")
    thumb_offset 0

style phone_chat_action_text is text:
    font "fonts/WorkSans-SemiBold.ttf"
    size 19
    bold True
    color "#ffffff"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5
    outlines []

# ── Typing dots animation ──
transform vip_gold_shimmer:
    alpha 0.2
    ease 1.2 alpha 0.7
    ease 1.2 alpha 0.2
    repeat

transform _typing_dot1:
    alpha 0.3
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.3
    pause 0.6
    repeat

transform _typing_dot2:
    alpha 0.3
    pause 0.2
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.3
    pause 0.4
    repeat

transform _typing_dot3:
    alpha 0.3
    pause 0.4
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.3
    pause 0.2
    repeat

# ============================================================
# CHAT ACTION MENUS (data: the screens below only draw them)
# ============================================================
init python:

    def _chat_tile(value, label, icon, color, free, note=None):
        """One tile of a chat action menu. value None = it is only there to say why not (`note`);
        free False = a typing pause is running, nothing can be tapped."""
        return {"value": value, "label": label, "icon": icon, "color": color, "note": note,
                "enabled": bool(free and value is not None)}

    def _chat_hangout_tile(group, free, value):
        """Hangout Night, or the reason it cannot be offered today. None = not an option for this group."""
        if hangout_can_invite(group):
            return _chat_tile(value, _tr("Hangout Night"), "glass", "#ec4899", free)
        for _blocked, _why in ((hangout_already_invited_today(), "already invited today"), (hangout_too_late(), "too late"),
                               (hangout_can_invite_no_bottle(group), "need to buy a bottle")):
            if _blocked:
                return _chat_tile(None, _tr("Hangout Night"), "glass", "#ec4899", free, _tr(_why))
        return None

    def phone_chat_actions(girl, auto_close=0.0):
        """Tiles of an open 1:1 chat, in menu order."""
        _free = auto_close <= 0
        _tiles = [_chat_tile("chat", _tl(_("Chat")), "bubble", "#22c55e", _free),
                  _chat_tile("flirt", _tl(_("Flirt")), "heart", "#f43f5e", _free),
                  _chat_tile(("invite" if girl.loc != CurrentLocation else None), _tl(_("Invite")), "home", "#3b82f6", _free)]
        _dinner = _tl(_("Invite to Dinner"))
        if restaurant_can_invite() and not restaurant_girl_already_invited(girl) and not restaurant_group_blocked(girl):
            _tiles.append(_chat_tile("dinner_invite", _dinner, "glass", "#f59e0b", _free))
        elif restaurant_girl_already_invited(girl):
            _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("already going"))))
        elif restaurant_dinner_full():
            _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("max 2 girls"))))
        elif restaurant_group_blocked(girl):
            _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("someone has a partner"))))
        elif restaurant_too_late():
            _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("too late"))))
        _tiles += [_chat_tile("video", _tl(_("Send Video")), "camera", "#fb923c", _free),
                   _chat_tile("dick_pic", _tl(_("Send Dick Pic")), "flame", "#ec4899", _free)]
        # his order to a submissive (player_phone_order.rpy): be in his room tonight
        _ppo_tile = player_phone_order_tile(girl, _free)
        if _ppo_tile:
            _tiles.append(_ppo_tile)
        return _tiles

    def phone_group_chat_actions(group, auto_close=0.0):
        """Tiles of an open group chat: harem group, girl + her partner, or a regular girl group."""
        _free = auto_close <= 0
        _n = len(group.get("members", []))
        _dinner = _tl(_("Dinner Together"))
        _tiles = []
        _invite = (lambda value: _chat_tile(value, _tl(_("Invite")), "home", "#3b82f6", _free))
        if _is_harem_group(group):
            _tiles.append(_chat_tile(("propose_member" if _harem_propose_candidates() else None), _tl(_("Propose Member")), "people", "#a78bfa", _free,
                                     (None if _harem_propose_candidates() else _tl(_("no candidates")))))
            _tiles += [_invite("invite"),
                       _chat_tile("video", _tl(_("Send Video")), "camera", "#fb923c", _free),
                       _chat_tile("group_dick_pic", _tl(_("Send Dick Pic")), "flame", "#ec4899", _free)]
            if _n <= 2 and restaurant_can_invite() and getattr(store, "_restaurant_day", -1) != store.Day:
                _tiles.append(_chat_tile("group_dinner", _dinner, "glass", "#f59e0b", _free))
            elif getattr(store, "_restaurant_day", -1) == store.Day:
                _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("already going"))))
            elif restaurant_too_late():
                _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("too late"))))
            elif _n > 2:
                _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("max 2 girls"))))
            _tiles.append(_chat_hangout_tile(group, _free, "hangout"))
        elif _group_has_partner(group):
            _tiles += [_invite("partner_invite"),
                       _chat_tile("partner_video", _tl(_("Send Video")), "camera", "#fb923c", _free),
                       _chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("max 2 girls"))),
                       _chat_hangout_tile(group, _free, "partner_hangout"),
                       _chat_tile("group_delete", _tl(_("Delete Group")), "broken", "#ef4444", _free)]
        else:
            _tiles += [_invite("invite"),
                       _chat_tile("video", _tl(_("Send Video")), "camera", "#fb923c", _free),
                       _chat_tile("group_dick_pic", _tl(_("Send Dick Pic")), "flame", "#ec4899", _free)]
            if _n >= 3:
                _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("max 2 girls"))))
            elif restaurant_can_invite() and getattr(store, "_restaurant_day", -1) != store.Day:
                _tiles.append(_chat_tile("dinner_group", _dinner, "glass", "#f59e0b", _free))
            elif getattr(store, "_restaurant_day", -1) == store.Day:
                _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("already invited"))))
            elif restaurant_too_late():
                _tiles.append(_chat_tile(None, _dinner, "glass", "#f59e0b", _free, _tl(_("too late"))))
            _tiles.append(_chat_hangout_tile(group, _free, "hangout"))
            # the player tidying duplicate groups (tester 2026-10-10); the harem group never offers it
            _tiles.append(_chat_tile("group_delete", _tl(_("Delete Group")), "broken", "#ef4444", _free))
        return [_tile for _tile in _tiles if _tile]

    def phone_chat_menu_height(tiles, choices):
        """Height of the action area of a chat: a grid of tiles (3 per row), or the answers (they scroll past 3)."""
        if choices is not None:
            _n = len(choices)
            return min(_n * 46 + max(0, _n - 1) * 6 + 16, 172) if _n else 0
        _rows = (len(tiles) + 2) // 3
        return _rows * 78 + max(0, _rows - 1) * 6 + 16 if _rows else 0

    def phone_chat_header_view(who):
        """(accent, [avatar], caption, caption color) of a 1:1 chat header: the same facts the contacts list shows."""
        try:
            _cv = phone_contact_view(who)
            return _cv["accent"], [_cv["avatar"]], (_cv["chip"][0] if _cv["chip"] else None), (_cv["chip"][1] if _cv["chip"] else None)
        except Exception as _e:
            print("[PHONE] chat header: no contact view for %r (%s)" % (getattr(who, "gid", who), _e))
            return "#4da6ff", ["images/menus/Char_Default.png"], None, None


# the action area both chat screens share: tiles of an open chat, or the answers of a chat event
screen phone_chat_menu(tiles, choices, top, tall):
    frame:
        xpos PH_CX
        ypos top
        xsize PH_CW
        ysize tall
        background "#0b1220"
        padding (8, 8, 8, 8)

        if choices is not None:
            viewport id "phone_action_vp":
                xsize PH_CW - 16 - 10
                ysize tall - 16
                mousewheel True
                draggable True
                vbox:
                    spacing 6
                    xsize PH_CW - 16 - 10
                    for _choice_item in choices:
                        $ _cl, _cv = _choice_item[0], _choice_item[1]
                        $ _c_disabled = (len(_choice_item) == 3 and _choice_item[2])
                        use pk_answer(_tr(_cl), Return(_cv), enabled=(not _c_disabled))
            vbar:
                style "pk_vscrollbar"
                value YScrollValue("phone_action_vp")
                thumb Solid("#3b82f6")
                xalign 1.0
                ysize tall - 16
        else:
            vbox:
                spacing 6
                xalign 0.5
                for _row in range(0, len(tiles), 3):
                    hbox:
                        spacing 6
                        xalign 0.5
                        for _tile in tiles[_row:_row + 3]:
                            use pk_tile(_tile["label"], _tile["icon"], _tile["color"], Return(_tile["value"]), enabled=_tile["enabled"], note=_tile["note"],
                                        width=int((PH_CW - 16 - 12) / 3))


screen phone_chat_screen(girl, auto_close=0.0, choices=None, can_leave=False):

    modal True
    zorder 200

    # He pressed Back / Home while she was still typing (_phone_leave_request): nothing waits for him again.
    # The rest of the typing goes by at once, and a screen with nothing to answer leaves with the button he pressed.
    $ _leave_btn = _phone_leave_button()
    if _leave_btn and auto_close > 0:
        timer 0.01 action Return("_typing_done")
    elif _leave_btn and not choices:
        timer 0.01 action [Function(_phone_leave_clear), Return(_leave_btn)]
    elif auto_close > 0:
        timer auto_close action Return("_typing_done")
        key "K_LCTRL" action Return("_typing_done")
        key "K_RCTRL" action Return("_typing_done")
    if choices:
        on "show" action Function(_phone_leave_clear)

    # Dark overlay
    button:
        xfill True
        yfill True
        background "#00000088"
        action NullAction()

    # Phone frame
    frame:
        xpos PH_X
        ypos PH_Y
        background None
        padding (0, 0)

        fixed:
            fit_first True
            add _phone_img

            # ── Header (phone UI kit): her face in a ring of her color, her name, what she is to him ──
            $ _hdr_y = PH_CY_STATUS
            $ _hdr_h = _PK_HEADER_H
            $ _ch_accent, _ch_faces, _ch_caption, _ch_caption_col = phone_chat_header_view(girl)
            use pk_chat_header(girl.Name, _ch_accent, _ch_faces, _hdr_y, _ch_caption, _ch_caption_col)

            # ── Chat body ────────────────────────────────
            $ _body_y = _hdr_y + _hdr_h
            $ _phone_bottom = _PH_SCREEN_BOTTOM
            python:
                _chat_tiles = phone_chat_actions(girl, auto_close) if choices is None else []
                _action_h = phone_chat_menu_height(_chat_tiles, choices)
            $ _action_y = _phone_bottom - _action_h
            $ _body_h = _action_y - _body_y

            frame:
                xpos PH_CX
                ypos _body_y
                xsize PH_CW
                ysize _body_h
                background "#060d11"
                padding (0, 0)

                viewport id "phone_chat_vp":
                    xpos 6
                    ypos 0
                    xsize PH_CW - 12
                    ysize _body_h
                    mousewheel True
                    draggable True
                    scrollbars None
                    yadjustment ui.adjustment(value=99999.0)

                    $ _grouped = _chat_build_grouped(girl.gid)
                    $ _vp_w = PH_CW - 12

                    vbox:
                        xsize _vp_w
                        yalign 1.0
                        spacing 0

                        null height 10

                        for _gm in _grouped:

                            # Day separator
                            if _gm["show_day"]:
                                null height 8
                                frame:
                                    style "phone_msg_day_chip"
                                    xalign 0.5
                                    text _gm["day_label"]:
                                        style "phone_text"
                                        size 14
                                        color "#ff9800"
                                null height 8

                            # Spacing between bubbles
                            null height _gm["spacing"]

                            # ── Typing indicator ──
                            if _gm["type"] == "typing":
                                frame:
                                    xalign 0.0
                                    xmaximum int(_vp_w * 0.35)
                                    yminimum 36
                                    background _BUBBLE_GIRL
                                    padding (14, 10, 14, 10)
                                    hbox:
                                        spacing 6
                                        yalign 0.5
                                        xalign 0.5
                                        text "\u2022" at _typing_dot1:
                                            size 24
                                            color "#0084FF"
                                        text "\u2022" at _typing_dot2:
                                            size 24
                                            color "#0084FF"
                                        text "\u2022" at _typing_dot3:
                                            size 24
                                            color "#0084FF"

                            # ── Player bubble (RIGHT) ──
                            elif _gm["sender"] == "player":
                                frame:
                                    xalign 1.0
                                    xmaximum int(_vp_w * 0.82)
                                    yminimum 36
                                    background _BUBBLE_PLAYER
                                    padding (14, 10, 14, 10)
                                    text _gm["text"]:
                                        style "phone_msg_player"

                            # ── System message ──
                            elif _gm["type"] == "system":
                                frame:
                                    style "phone_msg_day_chip"
                                    xalign 0.5
                                    text _gm["text"]:
                                        style "phone_text"
                                        size 14
                                        color "#ff9800"

                            # ── Girl photo bubble (LEFT) ──
                            elif _gm["type"] == "photo":
                                frame:
                                    xalign 0.0
                                    background None
                                    padding (0, 0)
                                    fixed:
                                        fit_first True
                                        add "images/menus/ChatGirl_Photo.png"
                                        add _gm["text"]:
                                            xalign 0.5
                                            yalign 0.5

                            # ── Girl bubble (LEFT) ──
                            else:
                                frame:
                                    xalign 0.0
                                    xmaximum int(_vp_w * 0.82)
                                    yminimum 36
                                    background _BUBBLE_GIRL
                                    padding (14, 10, 14, 10)
                                    text _gm["text"]:
                                        style "phone_msg_girl"

                        null height 8

            # ── Action menu (phone_chat_menu: tiles of an open chat, or the answers of a chat event) ──
            if _action_h > 0:
                use phone_chat_menu(_chat_tiles, choices, _action_y, _action_h)

            # ── Chin buttons (Back / Home) ──────────────
            # Choices of an EVENT (her question, a story text) must be answered: both buttons insensitive.
            # A BROWSE list he opened himself (the video picker, a flirt submenu) passes can_leave=True: Back
            # returns "close" and Home "home", the values its caller already handles (player report,
            # 2026-10-09: the SPECIAL video category had no way out).
            if choices and not can_leave:
                use phone_chin_buttons(back_action=None, home_action=False)
            else:
                use phone_chin_buttons(
                    back_action=_phone_leave_action("close", auto_close),
                    home_action=_phone_leave_action("home", auto_close))

# ============================================================
# CTRL-SKIP HELPER — True when Ctrl is held
# ============================================================
init python:
    # Back / Home pressed WHILE she is typing used to be swallowed: every caller ignores what a typing pause returns,
    # so the conversation went on and he had to press AGAIN at the end (player report, 2026-09-19). The press is now
    # remembered for a moment. Both chat screens read it (their first lines).
    _PHONE_LEAVE_WINDOW = 3.0       # seconds: with the request on, the rest of a conversation runs in milliseconds

    def _phone_leave_request(button):
        import time
        store._phone_leave_pending = (button, time.time())
        print("[PHONE] %s pressed during a typing pause: leaving as soon as nothing needs an answer" % button)

    def _phone_leave_button():
        """"close" / "home" when he asked to leave during a typing pause moments ago, else None."""
        import time
        _p = getattr(store, "_phone_leave_pending", None)
        if _p and 0 <= time.time() - _p[1] < _PHONE_LEAVE_WINDOW:
            return _p[0]
        return None

    def _phone_leave_clear():
        store._phone_leave_pending = None

    def _phone_leave_action(button, auto_close):
        """Action of the Back / Home buttons of a chat screen. During a typing pause the press is also remembered."""
        if auto_close > 0:
            return [Function(_phone_leave_request, button), Return(button)]
        return Return(button)

    def _phone_ctrl_held():
        import pygame
        mods = pygame.key.get_mods()
        return bool(mods & (pygame.KMOD_LCTRL | pygame.KMOD_RCTRL))

# ============================================================
# TYPING ANIMATION — uses call screen with auto_close timer
# ============================================================
label _phone_typing(girl, choices=None):
    if _phone_ctrl_held():
        return
    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    $ _typing_delay = renpy.random.uniform(0.8, 1.4)
    if choices is not None:
        call screen phone_chat_screen(girl, auto_close=_typing_delay, choices=choices)
    else:
        call screen phone_chat_screen(girl, auto_close=_typing_delay)
    python:
        _t_msgs = phone_get_msgs(girl.gid)
        if _t_msgs and _t_msgs[-1].get("type") == "typing":
            _t_msgs.pop()
    return

# ============================================================
# REPLAY QUEUED MESSAGES — one-by-one with typing animation
# ============================================================
label _phone_replay_queue(girl):
    python:
        _pq = list(getattr(store, "_phone_msg_queue", []))
        store._phone_msg_queue = []

label ._pq_loop:
    if not _pq:
        return
    python:
        _pq_msg = _pq.pop(0)
        _pq_sender = _pq_msg["sender"]
        _pq_gid = _pq_msg["gid"]
        _pq_text = _pq_msg["text"]
    if _pq_sender != "player" and not _phone_ctrl_held():
        call _phone_typing(girl) from _replay_typing_q
    $ phone_add_msg(_pq_gid, _pq_sender, _pq_text)
    if _pq_sender != "player" and _pq and not _phone_ctrl_held():
        call screen phone_chat_screen(girl, auto_close=0.4)
    jump ._pq_loop

# ============================================================
# CHAT FLOW LABEL
# ============================================================

label phone_open_chat(girl):

    $ store._phone_chat_exit = "back"
    $ store._phone_chat_girl = girl

    # Girl is in the same location — no need to text
    if girl.loc == CurrentLocation:
        $ phone_add_msg(girl.gid, "player", _tl(_("Hey")))
        call _phone_typing(girl) from _typing_same_loc
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("I'm right here, silly. Just talk to me.")))
        call screen phone_chat_screen(girl, choices=[])
        return

    # Ex who hasn't had the cheating confrontation — refuses all messages
    if hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
        $ phone_add_msg(girl.gid, "player", _tl(_("Hey...")))
        call _phone_typing(girl) from _typing_ex_unresolved
        python:
            _ex_phone_block = [
                _("Don't text me. I can't even look at your name on my screen right now."),
                _("I have nothing to say to you. Not like this. Not through a phone."),
                _("You want to talk? Then come find me. I'm not doing this over text."),
            ]
            phone_add_msg(girl.gid, girl.gid, _tl(renpy.random.choice(_ex_phone_block)))
        call screen phone_chat_screen(girl)
        return

    # Angry/sad girl refuses
    if hasattr(girl, "has_temp_status") and girl.has_temp_status("angry"):
        $ phone_add_msg(girl.gid, "player", _tl(_("Hey")))
        call _phone_typing(girl) from _typing_angry
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("I don't want to talk to you right now.")))
        call screen phone_chat_screen(girl)
        return

    if hasattr(girl, "has_temp_status") and girl.has_temp_status("sad"):
        $ phone_add_msg(girl.gid, "player", _tl(_("Hey, are you okay?")))
        call _phone_typing(girl) from _typing_sad
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("I... can't talk right now. Sorry.")))
        call screen phone_chat_screen(girl)
        return

    if getattr(girl, "_giving_birth", False):
        $ phone_add_msg(girl.gid, "player", _tl(_("Hey")))
        call _phone_typing(girl) from _typing_birth
        $ phone_add_msg(girl.gid, girl.gid, _tl(renpy.random.choice(girl_pool(_CHILD_AWAY_AUTOREPLY, girl, "away auto-reply"))))
        call screen phone_chat_screen(girl)
        return

    label .chat_loop:

    # invariant: the open chat never runs in phone mode (it is only on while a reaction queues its lines);
    # a crash inside one of the flows below must never leave it stuck on
    $ _phone_mode_off()

    call screen phone_chat_screen(girl)
    $ _chat_action = _return

    if _chat_action == "home":
        $ store._phone_chat_exit = "home"
        $ _phone_restore_others()
        return

    if _chat_action == "chat":
        python:
            _pl = _tl(renpy.random.choice(_PHONE_CHAT_PLAYER_LINES))
            phone_add_msg(girl.gid, "player", _pl)
        call _phone_typing(girl) from _typing_chat
        python:
            store._phone_msg_queue = []
            # finally: a crash inside the topic must NEVER leave phone mode on (it swallows every Say_Line /
            # Narration of the whole game afterwards: the "100% locked" player report, 2026-10-09)
            _phone_mode_on(girl)
            try:
                _cc_func = pick_chitchat_func(girl, CurrentLocation, TimeIndex)
                _cc_func(girl, CurrentLocation, TimeIndex)
            finally:
                _phone_mode_off()
        # Replay queued messages one-by-one with typing animation
        call _phone_replay_queue(girl) from _replay_chat
        jump .chat_loop

    elif _chat_action == "flirt":
        # Step 1: Compliment or Joke
        $ _flirt_main = [(_("Compliment her"), "compliment"), (_("Make a joke"), "joke")]
        call screen phone_chat_screen(girl, choices=_flirt_main, can_leave=True)
        $ _flirt_pick = _return

        if _flirt_pick == "home":
            $ store._phone_chat_exit = "home"
            $ _phone_restore_others()
            return
        if _flirt_pick == "close":
            jump .chat_loop

        if _flirt_pick == "joke":
            python:
                _joke_lines_good = [
                    _("Why did the student bring a ladder? To reach high grades!"),
                    _("I'd tell you a chemistry joke, but I'd get no reaction."),
                    _("Are you a magician? Because whenever I look at you, everyone else disappears."),
                    _("I'm reading a book about anti-gravity. It's impossible to put down."),
                    _("Do you have a map? I keep getting lost in this conversation."),
                ]
                _joke_lines_bad = [
                    _("Why did the chicken cross the road? ...nevermind."),
                    _("Knock knock... actually forget it, it's not that funny."),
                    _("I had a joke but I forgot the punchline..."),
                    _("What do you call a... uh... yeah I got nothing."),
                ]
                _joke_result = do_safe_flirt(girl, "joke")
                _joke_reaction = get_flirt_reaction_mode_safe(girl, _joke_result, "joke")
                if _joke_result == "ok":
                    _joke_player = _tl(renpy.random.choice(_joke_lines_good))
                else:
                    _joke_player = _tl(renpy.random.choice(_joke_lines_bad))
                phone_add_msg(girl.gid, "player", _joke_player)
                _joke_resp = _phone_get_flirt_text(girl, "safe_joke", _joke_reaction)
            call _phone_typing(girl) from _typing_joke
            $ phone_add_msg(girl.gid, girl.gid, _joke_resp)
            $ _rod_flirt_discover(girl, _joke_reaction)
            jump .chat_loop

        # Step 2: Pick a compliment (no Back button here)
        python:
            _comp_pool = list(COMPLIMENT_OPTIONS)
            renpy.random.shuffle(_comp_pool)
            _comp_choices = []
            _comp_data = {}
            for _i, (_ck, _ct, _ckind) in enumerate(_comp_pool[:3]):
                _cval = "comp_%d" % _i
                _comp_choices.append((_tl(_ct), _cval))
                _comp_data[_cval] = (_ck, _tl(_ct), _ckind)

        call screen phone_chat_screen(girl, choices=_comp_choices, can_leave=True)
        $ _comp_pick = _return

        if _comp_pick == "home":
            $ store._phone_chat_exit = "home"
            $ _phone_restore_others()
            return
        if _comp_pick == "close":
            jump .chat_loop

        python:
            _phone_comp_key, _phone_comp_text, _phone_comp_kind = _comp_data[_comp_pick]
            _act_key = "compliment_%s" % _phone_comp_key
            phone_add_msg(girl.gid, "player", _phone_comp_text)
            if _phone_comp_kind == "safe":
                _comp_result = do_safe_flirt(girl, _act_key)
                _comp_reaction = get_flirt_reaction_mode_safe(girl, _comp_result, _act_key)
                _comp_resp = _phone_get_flirt_text(girl, "safe_%s" % _act_key, _comp_reaction)
            else:
                _comp_result_l = do_lewd_flirt_approval(girl, _act_key, T=950, Type="LI", Spread=170, Bonus=0, Variation=60)
                _comp_reaction = get_flirt_reaction_mode_lewd(girl, _comp_result_l, _act_key)
                _comp_resp = _phone_get_flirt_text(girl, "lewd_%s" % _act_key, _comp_reaction)
        call _phone_typing(girl) from _typing_comp
        $ phone_add_msg(girl.gid, girl.gid, _comp_resp)
        $ _rod_flirt_discover(girl, _comp_reaction)
        python:
            # her personality after the answer (a compliment she loves / distrusts): the same rule as face to face
            _comp_aside = persona_flirt_aside(girl, "safe_%s" % _act_key, _comp_reaction) if _phone_comp_kind == "safe" else None
            if _comp_aside:
                phone_add_msg(girl.gid, girl.gid, _tl(_comp_aside[1]))
        jump .chat_loop

    elif _chat_action == "order":
        call _player_phone_order_event(girl) from _call_player_phone_order_event
        jump .chat_loop

    elif _chat_action == "invite":
        python:
            phone_add_msg(girl.gid, "player", _tl(_("Want to come hang out with me?")))
            _fi_result, _fi_reason = _girl_accepts_invite(girl)
            _will_come = _fi_result
            _PHONE_INVITE_JEALOUS = [
                _("I don't really feel like seeing you right now. Maybe later."),
                _("Not today. I need some time to myself."),
                _("I'll pass. Go invite someone else, I'm sure you have options."),
            ]
            if _will_come and girl.is_dating_player() and getattr(girl, "Jealousy", 0) >= 600:
                if not (girl.has_trait("polyamorous") or is_player_harem_exempt(girl)):
                    _will_come = False
                    _fi_reason = "jealous"
                    print("[JEALOUSY] %s refused phone invite (Jealousy=%d)" % (girl.gid, getattr(girl, "Jealousy", 0)))
        call _phone_typing(girl) from _typing_invite
        if _will_come:
            python:
                _acc = _tl(renpy.random.choice(_PHONE_INVITE_ACCEPT))
                phone_add_msg(girl.gid, girl.gid, _acc)
                phone_add_msg(girl.gid, "system", _tl(_("%s is on her way.")) % girl.Name)
                girl.loc = CurrentLocation
                _girls_now = [_g for _g in ALL_GIRLS if _g.loc == CurrentLocation]
                _npc_here = getattr(store, "_npc_on_scene", None)
                build_location_roster(_girls_now, _npc_here)
                _sprite_suppressed.discard(girl.Id)
                show_roster_sprites()
                store._phone_girl_arrived = girl.gid
        else:
            python:
                if _fi_reason == "jealous":
                    _dec = _tl(renpy.random.choice(_PHONE_INVITE_JEALOUS))
                else:
                    _fi_pool = FOLLOW_INVITE_DECLINE.get(_fi_reason, _PHONE_INVITE_DECLINE)
                    _fi_raw = renpy.random.choice(_fi_pool)
                    if _fi_reason in _FOLLOW_DECLINE_PARTNER_FMT:
                        _dec = _format_partner_line(girl, _fi_raw)
                    else:
                        _dec = _tl(_fi_raw)
                phone_add_msg(girl.gid, girl.gid, _dec)
        jump .chat_loop

    elif _chat_action == "dinner_invite":
        call restaurant_send_solo_invite(girl) from _call_rest_solo_invite
        jump .chat_loop

    elif _chat_action == "photo":
        python:
            phone_add_msg(girl.gid, "player", _tl(_("Send me a photo? ;)")))
            _pvs_fn = globals().get("pregnancy_visual_stage")
            # a "no_photos" girl speaks her permanent rule (photo_never), not the pregnancy excuse: the excuse
            # implies she would send one otherwise (_photo_decide answers "no_photos" first)
            _preg_photo_block = callable(_pvs_fn) and _pvs_fn(girl) >= 1 and girl_sends_photos(girl)
            if not _preg_photo_block:
                _approval = _photo_decide(girl)
        call _phone_typing(girl) from _typing_photo
        if _preg_photo_block:
            python:
                _preg_deny = [
                    _("Not right now... I'm not feeling great about how I look."),
                    _("Maybe later? I just... don't want to take photos right now."),
                    _("I'd rather not... my body is going through some changes."),
                ]
                phone_add_msg(girl.gid, girl.gid, _tl(renpy.random.choice(_preg_deny)))
            jump .chat_loop
        if _approval["accepted"]:
            $ _photo_save(girl)
            call screen phone_show_photo(girl)
            python:
                _accept_line = _photo_get_accept_line(girl)
                phone_add_msg(girl.gid, girl.gid, _accept_line, "photo")
                Change_Status(girl, "Inbt", 3)
                if girl.has_trait("camera_lover"):
                    Change_Status(girl, "Love", 3)
                if store._photo_chest is None and store._photo_over is None:
                    girl.RegisterAction("photo_sent_topless")
                if store._photo_panties is None and store._photo_legs is None:
                    girl.RegisterAction("photo_sent_bottomless")
                girl.RegisterAction("photo_sent")
        else:
            python:
                _deny_line = _photo_get_deny_line(girl, _approval["reason"])
                phone_add_msg(girl.gid, girl.gid, _deny_line)
                if _approval["reason"] == "camera_hater":
                    Change_Status(girl, "Love", -5)
        jump .chat_loop

    elif _chat_action == "video":
        python:
            _vids = getattr(store.Player, "recorded_videos", [])
        if not _vids:
            $ phone_add_msg(girl.gid, "system", _("You don't have any recorded videos."))
            jump .chat_loop

        # Step 1: Pick girl from videos
        python:
            _girl_gids = sorted(set(v["girl_gid"] for v in _vids))
            _vid_girl_choices = []
            for _gid in _girl_gids:
                _cg = GIRL_BY_ID.get(_gid)
                if _cg:
                    _vid_girl_choices.append((_cg.Name, _gid))
        call screen phone_chat_screen(girl, choices=_vid_girl_choices, can_leave=True)
        $ _chosen_gid = _return
        if _chosen_gid == "home":
            $ store._phone_chat_exit = "home"
            $ _phone_restore_others()
            return
        if _chosen_gid in (None, "close"):
            jump .chat_loop

        # Step 2: Pick position (split by face_hidden, + SPECIAL category)
        python:
            _gid_vids = [v for v in _vids if v["girl_gid"] == _chosen_gid]
            _combos = set()
            for _cv in _gid_vids:
                if _cv.get("special"):
                    continue
                _var = "nc" if not _cv.get("consensual", True) else ("h" if _cv.get("face_hidden", True) else "v")
                _combos.add((_cv["type"], _var))
            _combos = sorted(_combos)
            _vid_pos_choices = []
            for _pos, _var in _combos:
                _label = _pk_t(VIDEO_TYPE_DISPLAY.get(_pos, _pos.replace("_", " ").title()))
                if _var == "nc":
                    _label += " {size=18}(" + _tl(_("non-consensual")) + "){/size}"
                elif _var == "h":
                    _label += " {size=18}(" + _tl(_("hidden face")) + "){/size}"
                else:
                    _label += " {size=18}(" + _("face visible") + "){/size}"
                _vid_pos_choices.append((_label, _pos + "|" + _var))
            _has_special = any(v.get("special") for v in _gid_vids)
            if _has_special:
                _vid_pos_choices.append((_("SPECIAL"), "special"))
        call screen phone_chat_screen(girl, choices=_vid_pos_choices, can_leave=True)
        $ _chosen_pos = _return
        if _chosen_pos == "home":
            $ store._phone_chat_exit = "home"
            $ _phone_restore_others()
            return
        if _chosen_pos in (None, "close"):
            jump .chat_loop

        # Parse variant from choice value
        python:
            _chosen_face_hidden = None
            _chosen_nonconsensual = False
            if _chosen_pos and "|" in str(_chosen_pos):
                _pparts = _chosen_pos.split("|")
                _chosen_pos = _pparts[0]
                if _pparts[1] == "nc":
                    _chosen_nonconsensual = True
                elif _pparts[1] == "h":
                    _chosen_face_hidden = True
                else:
                    _chosen_face_hidden = False

        # Step 2b: If SPECIAL, pick the specific special type
        if _chosen_pos == "special":
            python:
                _special_types = sorted(set(v.get("special") for v in _gid_vids if v.get("special")))
                _special_choices = [(SPECIAL_VIDEO_DISPLAY.get(s, s.title()), s) for s in _special_types]
            call screen phone_chat_screen(girl, choices=_special_choices, can_leave=True)
            $ _chosen_special = _return
            if _chosen_special == "home":
                $ store._phone_chat_exit = "home"
                $ _phone_restore_others()
                return
            if _chosen_special in (None, "close"):
                jump .chat_loop

        # Step 3: Pick location (if multiple)
        python:
            if _chosen_pos == "special":
                _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v.get("special") == _chosen_special]
            elif _chosen_nonconsensual:
                _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v["type"] == _chosen_pos and not v.get("special") and not v.get("consensual", True)]
            else:
                _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v["type"] == _chosen_pos and not v.get("special") and v.get("consensual", True)]
                if _chosen_face_hidden is not None:
                    _matching = [v for v in _matching if v.get("face_hidden", True) == _chosen_face_hidden]
            _locs = sorted(set(v.get("location", "unknown") for v in _matching))
        if len(_locs) > 1:
            python:
                _VID_LOC_NAMES = {
                    "campus": _tr("Campus"), "pool": _tr("Pool"), "showers": _tr("Showers"), "apartment": _tr("Apartment"), "apartment_room": _tr("Apartment Bedroom"), "apartment_shower": _tr("Apartment Bathroom"),
                    "room": _tr("%s's Room") % store.Player.Name,
                    "gwen_room": _tr("Gwen's Room"), "rogue_room": _tr("Rogue's Room"), "ntw_room": _tr("Negasonic's Room"), "tenny_room": _tr("%s's Room") % GIRL_BY_ID["tenny"].Name,
                    "classroom": _tr("Classroom"), "gym": _tr("Gym"), "hall": _tr("Hall"),
                    "street": _tr("Street"), "mall": _tr("Mall"), "party": _tr("Party"),
                }
                _vid_loc_choices = [(_VID_LOC_NAMES.get(l, l.replace("_", " ").title()), l) for l in _locs]
            call screen phone_chat_screen(girl, choices=_vid_loc_choices, can_leave=True)
            $ _chosen_loc = _return
            if _chosen_loc == "home":
                $ store._phone_chat_exit = "home"
                $ _phone_restore_others()
                return
        else:
            $ _chosen_loc = _locs[0] if _locs else None

        if _chosen_loc in (None, "close"):
            jump .chat_loop

        # Step 4: Condom choice (only for RCG/cowgirl when both versions exist)
        python:
            _loc_vids = [v for v in _matching if v.get("location", "") == _chosen_loc]
            _has_condom = any(v.get("condom", False) for v in _loc_vids)
            _has_raw = any(v.get("condom") == False and "condom" in v for v in _loc_vids)
            _show_condom_choice = _chosen_pos in (_("cowgirl"), "reverse_cowgirl") and _has_condom and _has_raw
            _chosen_condom = None
        if _show_condom_choice:
            call screen phone_chat_screen(girl, choices=[("Condom", True), ("Raw", False)], can_leave=True)
            $ _chosen_condom = _return
            if _chosen_condom == "home":
                $ store._phone_chat_exit = "home"
                $ _phone_restore_others()
                return
            if _chosen_condom in (None, "close"):
                jump .chat_loop

        # Send the video
        python:
            _sent_vid = None
            for _v in reversed(_loc_vids if _loc_vids else _matching):
                if _v.get("location", "") == _chosen_loc:
                    if _show_condom_choice:
                        if _v.get("condom") == _chosen_condom:
                            _sent_vid = _v
                            break
                    else:
                        _sent_vid = _v
                        break
            if _sent_vid is None:
                _sent_vid = _matching[-1] if _matching else {"girl_gid": _chosen_gid, "type": _chosen_pos, "location": _chosen_loc, "consensual": True}
            _vid_girl = GIRL_BY_ID.get(_chosen_gid)
            _vid_name = _vid_girl.Name if _vid_girl else "someone"
            _vid_loc = _sent_vid.get("location", "room")
            _vid_loc_names = {
                "room": _("in your room"), "campus": _("on campus"), "pool": _("at the pool"),
                "hall": _("in the hallway"), "street": _("on the street"), "mall": _("at the mall"),
                "party": _("at the party"), "gym": _("at the gym"), "classroom": _("in the classroom"),
                "showers": _("in the showers"), "apartment": _("in the apartment"), "apartment_room": _("in the bedroom"), "apartment_shower": _("in the bathroom"), "shower": _("in the shower"), "bathroom": _("in the bathroom"),
                "library": _("in the library"), "dorm": _("in the dorm"), "kitchen": _("in the kitchen"),
                "park": _("at the park"), "beach": _("at the beach"), "car": _("in the car"),
                "office": _("in the office"), "rooftop": _("on the rooftop"),
                "gwen_room": _("in a dorm room"), "rogue_room": _("in a dorm room"), "ntw_room": _("in a dorm room"),
            }
            if _vid_loc == _chosen_gid + "_room":
                _vid_loc_names[_vid_loc] = _("in her room")
            _vid_loc_str = _tl(_vid_loc_names.get(_vid_loc, "in " + _vid_loc.replace("_", " ")))
            _vid_send_descs = {
                "hj": renpy.random.choice([
                    _("You sent a video of %s jerking you off %s"),
                    _("You sent a video of %s stroking your cock %s"),
                    _("You sent a video of %s's hand wrapped around you %s"),
                ]),
                "bj": renpy.random.choice([
                    _("You sent a video of %s sucking your dick %s"),
                    _("You sent a video of %s going down on you %s"),
                    _("You sent a video of %s with her lips around your cock %s"),
                ]),
                "tj": renpy.random.choice([
                    _("You sent a video of %s's tits wrapped around your dick %s"),
                    _("You sent a video of your cock between %s's tits %s"),
                    _("You sent a video of %s giving you a titjob %s"),
                ]),
                "cowgirl": renpy.random.choice([
                    _("You sent a video of %s riding you %s"),
                    _("You sent a video of %s bouncing on your cock %s"),
                    _("You sent a video of %s on top of you %s"),
                ]),
                "reverse_cowgirl": renpy.random.choice([
                    _("You sent a video of %s riding you facing away %s"),
                    _("You sent a video of %s bouncing on you with her back turned %s"),
                    _("You sent a video of %s on top, facing the other way %s"),
                ]),
                "creampie": renpy.random.choice([
                    _("You sent a video of you cumming inside %s %s"),
                    _("You sent a video of you finishing deep inside %s %s"),
                    _("You sent a video of you filling %s up %s"),
                ]),
                "masturbate": renpy.random.choice([
                    _("You sent a video of %s touching herself %s"),
                    _("You sent a video of %s pleasuring herself %s"),
                    _("You sent a video of %s playing with herself %s"),
                ]),
                "sex": renpy.random.choice([
                    _("You sent a video of you fucking %s %s"),
                    _("You sent a video of you and %s going at it %s"),
                    _("You sent a video of you deep inside %s %s"),
                ]),
                "anal": renpy.random.choice([
                    _("You sent a video of you doing anal with %s %s"),
                    _("You sent a video of you taking %s's ass %s"),
                    _("You sent a video of you inside %s's tight ass %s"),
                ]),
                "laying_down": renpy.random.choice([
                    _("You sent a video of you on top of %s %s"),
                    _("You sent a video of %s pinned under you %s"),
                    _("You sent a video of you pressing %s into the bed %s"),
                ]),
                "laying_anal": renpy.random.choice([
                    _("You sent a video of you doing anal with %s while on top %s"),
                    _("You sent a video of you in %s's ass while she's pinned down %s"),
                    _("You sent a video of you taking %s's ass from above %s"),
                ]),
                "reverse_cowgirl_anal": renpy.random.choice([
                    _("You sent a video of %s riding you in reverse with it in her ass %s"),
                    _("You sent a video of %s taking it in the ass on top of you %s"),
                ]),
            }
            # Special video descriptions
            _special_type = _sent_vid.get("special")
            if _special_type == "virginity":
                _vid_send_msg = _tl(_("You sent a video of %s losing her virginity %s")) % (_vid_name, _vid_loc_str)
            else:
                _vid_send_msg = _tl(_vid_send_descs.get(_chosen_pos, _("You sent a video of %s %s"))) % (_vid_name, _vid_loc_str)
            phone_add_msg(girl.gid, "player", _vid_send_msg, "system")
        call _phone_typing(girl) from _typing_video
        python:
            store._phone_msg_queue = []
            _phone_mode_on(girl)
            try:
                video_reaction(girl, _sent_vid)
            finally:
                _phone_mode_off()
        call _phone_replay_queue(girl) from _replay_video
        jump .chat_loop

    elif _chat_action == "dick_pic":
        $ _dp_result = _dp_process_dickpic(girl)
        if _dp_result is None:
            $ phone_add_msg(girl.gid, "system", _tl(_("You already sent one today. Give her some time.")), "system")
            jump .chat_loop

        $ phone_add_msg(girl.gid, "player", _tl(_("You sent a photo.")), "system")
        call _phone_typing(girl) from _typing_dickpic
        $ phone_add_msg(girl.gid, girl.gid, _dp_result["line"])
        jump .chat_loop

    # "close" (back button) or anything else
    $ store._phone_chat_exit = "back"
    return

# ============================================================
# GROUP CHAT SCREEN
# ============================================================

screen phone_group_chat_screen(group, auto_close=0.0, choices=None):

    modal True
    zorder 200

    # He pressed Back / Home while she was still typing (_phone_leave_request): nothing waits for him again.
    # The rest of the typing goes by at once, and a screen with nothing to answer leaves with the button he pressed.
    $ _leave_btn = _phone_leave_button()
    if _leave_btn and auto_close > 0:
        timer 0.01 action Return("_typing_done")
    elif _leave_btn and not choices:
        timer 0.01 action [Function(_phone_leave_clear), Return(_leave_btn)]
    elif auto_close > 0:
        timer auto_close action Return("_typing_done")
        key "K_LCTRL" action Return("_typing_done")
        key "K_RCTRL" action Return("_typing_done")
    if choices:
        on "show" action Function(_phone_leave_clear)

    button:
        xfill True
        yfill True
        background "#00000088"
        action NullAction()

    frame:
        xpos PH_X
        ypos PH_Y
        background None
        padding (0, 0)

        fixed:
            fit_first True
            add _phone_img

            # ── Header (phone UI kit): the first members' faces, the group name, who is in it ──
            $ _hdr_y = PH_CY_STATUS
            $ _hdr_h = _PK_HEADER_H
            $ _grp_members = group["members"]
            $ _grp_name = group["name"]
            use pk_chat_header(_grp_name, "#a78bfa", [_girl_avatar_by_gid(_mg) for _mg in _grp_members[:3]], _hdr_y,
                               format_name_list([_girl_name_by_gid(_m) for _m in _grp_members]))

            # ── Chat body ────────────────────────────────
            $ _body_y = _hdr_y + _hdr_h
            $ _phone_bottom = _PH_SCREEN_BOTTOM
            python:
                _chat_tiles = phone_group_chat_actions(group, auto_close) if choices is None else []
                _action_h = phone_chat_menu_height(_chat_tiles, choices)
                _action_y = _phone_bottom - _action_h
                _body_h = _action_y - _body_y

            frame:
                xpos PH_CX
                ypos _body_y
                xsize PH_CW
                ysize _body_h
                background "#060d11"
                padding (0, 0)

                viewport id "phone_group_chat_vp":
                    xpos 6
                    ypos 0
                    xsize PH_CW - 12
                    ysize _body_h
                    mousewheel True
                    draggable True
                    scrollbars None
                    yadjustment ui.adjustment(value=99999.0)

                    $ _grouped = _group_chat_build_grouped(group["id"])
                    $ _vp_w = PH_CW - 12

                    vbox:
                        xsize _vp_w
                        yalign 1.0
                        spacing 0

                        null height 10

                        for _gm in _grouped:

                            # Day separator
                            if _gm["show_day"]:
                                null height 8
                                frame:
                                    style "phone_msg_day_chip"
                                    xalign 0.5
                                    text _gm["day_label"]:
                                        style "phone_text"
                                        size 14
                                        color "#ff9800"
                                null height 8

                            null height _gm["spacing"]

                            # ── Player bubble (RIGHT) ──
                            if _gm["sender"] == "player":
                                frame:
                                    xalign 1.0
                                    xmaximum int(_vp_w * 0.82)
                                    yminimum 36
                                    background _BUBBLE_PLAYER
                                    padding (14, 10, 14, 10)
                                    text _gm["text"]:
                                        style "phone_msg_player"

                            # ── System message ──
                            elif _gm["type"] == "system":
                                frame:
                                    style "phone_msg_day_chip"
                                    xalign 0.5
                                    text _gm["text"]:
                                        style "phone_text"
                                        size 14
                                        color "#ff9800"

                            # ── Typing indicator ──
                            elif _gm["type"] == "typing":
                                $ _t_gid = _gm["sender"]
                                $ _t_avatar = _girl_avatar_by_gid(_t_gid)
                                $ _t_bubble = _group_bubble_for(_t_gid)
                                hbox:
                                    spacing 6
                                    xalign 0.0
                                    add _t_avatar:
                                        yalign 0.5
                                        zoom 0.28
                                    frame:
                                        xmaximum int(_vp_w * 0.35)
                                        yminimum 36
                                        background _t_bubble
                                        padding (14, 10, 14, 10)
                                        hbox:
                                            spacing 6
                                            yalign 0.5
                                            xalign 0.5
                                            text "\u2022" at _typing_dot1:
                                                size 24
                                                color "#ffffff"
                                            text "\u2022" at _typing_dot2:
                                                size 24
                                                color "#ffffff"
                                            text "\u2022" at _typing_dot3:
                                                size 24
                                                color "#ffffff"

                            # ── Girl bubble (LEFT) with avatar + name ──
                            else:
                                $ _sender_gid = _gm["sender"]
                                $ _sender_name = _girl_name_by_gid(_sender_gid)
                                $ _sender_avatar = _girl_avatar_by_gid(_sender_gid)
                                $ _sender_bubble = _group_bubble_for(_sender_gid)

                                hbox:
                                    spacing 6
                                    xalign 0.0
                                    xmaximum int(_vp_w * 0.88)

                                    # Girl avatar
                                    add _sender_avatar:
                                        yalign 0.0
                                        zoom 0.28

                                    vbox:
                                        spacing 2

                                        # Girl name label (only on first/solo of group)
                                        if _gm["group"] in ("first", "solo"):
                                            text _sender_name:
                                                style "phone_text"
                                                size 13
                                                color "#8ca0b4"

                                        # Message bubble
                                        frame:
                                            xmaximum int(_vp_w * 0.72)
                                            yminimum 36
                                            background _sender_bubble
                                            padding (14, 10, 14, 10)
                                            text _gm["text"]:
                                                style "phone_msg_player"

                        null height 8

            # ── Action menu (phone_chat_menu: tiles of an open chat, or the answers of a chat event) ──
            if _action_h > 0:
                use phone_chat_menu(_chat_tiles, choices, _action_y, _action_h)

            # ── Chin buttons ──
            use phone_chin_buttons(
                back_action=_phone_leave_action("close", auto_close),
                home_action=_phone_leave_action("home", auto_close))

# ============================================================
# GROUP CREATION SCREEN
# ============================================================

screen phone_create_group_screen():

    modal True
    zorder 200

    # Track selected girls
    default _selected_gids = set()

    $ _ng_accent = "#a78bfa"
    $ _ng_btn_h = 58
    $ _ng_body_y = PH_CY_HEADER + _PK_HEADER_H + 8
    $ _ng_btn_y = _PH_SCREEN_BOTTOM - _ng_btn_h - 10
    $ _ng_body_h = _ng_btn_y - _ng_body_y - 8
    $ _can_create = len(_selected_gids) >= 2

    use pk_page():

        use pk_header(_tl(_("New Group")), _ng_accent, "people"):
            use pk_chip("%d/3" % len(_selected_gids), (_ng_accent if _can_create else _PK_MUTED))

        viewport:
            id "ng_vp"
            xpos PH_CX
            ypos _ng_body_y
            xsize PH_CW
            ysize _ng_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 8
                xsize PH_CW - 14

                text _("Select members (2-3):"):
                    style "phone_text"
                    font "fonts/WorkSans-Medium.ttf"
                    size 15
                    color _PK_MUTED
                    xpos 12

                for _cg in _group_create_candidates():
                    $ _cg_gid = _cg.gid
                    $ _cg_is_npc = _cg_gid.startswith("npc_")
                    $ _has_contact = (_cg_gid in getattr(Player, "phone_npc_contacts", set())) if _cg_is_npc else (_cg_gid in getattr(Player, "phone_contacts", set()))
                    $ _is_sel = _cg_gid in _selected_gids
                    $ _cand_ok = _has_contact and _group_cand_allowed(_cg_gid, _selected_gids)
                    $ _cg_col = (getattr(_cg, "color", None) or _ng_accent) if not _cg_is_npc else "#7ecbff"

                    button:
                        xsize _PK_CARD_W
                        xalign 0.5
                        sensitive _cand_ok
                        padding (12, 9, 14, 9)
                        background _pk_card_bg(_ng_accent if _is_sel else None)
                        hover_background _pk_card_bg(_ng_accent)
                        action ToggleSetMembership(_selected_gids, _cg_gid)

                        hbox:
                            xfill True
                            hbox:
                                spacing 14
                                yalign 0.5
                                fixed:
                                    xsize 52
                                    ysize 52
                                    yalign 0.5
                                    add Transform(_pk_tint(_PK_RING, (_cg_col if _cand_ok else _PK_DIM)), xysize=(52, 52))
                                    add _pk_face(_girl_avatar_by_gid(_cg_gid), 44) align (0.5, 0.5) alpha (1.0 if _cand_ok else 0.45)
                                vbox:
                                    yalign 0.5
                                    spacing 3
                                    text _cg.Name:
                                        style "phone_text"
                                        size 19
                                        bold True
                                        color (_PK_TEXT if _cand_ok else _PK_DIM)
                                    if _cg_is_npc:
                                        text _npc_partner_label(_cg_gid):
                                            style "phone_text"
                                            font "fonts/WorkSans-Medium.ttf"
                                            size 13
                                            color (_PK_MUTED if _cand_ok else _PK_DIM)
                                    if not _has_contact:
                                        text _("(no number)"):
                                            style "phone_text"
                                            font "fonts/WorkSans-Medium.ttf"
                                            size 13
                                            color _PK_DIM
                            # selection mark: a filled plate with the check when she is in
                            frame:
                                xsize 30
                                ysize 30
                                xalign 1.0
                                yalign 0.5
                                padding (0, 0)
                                background _pk_pill((_ng_accent if _is_sel else "#64748b"), (0.9 if _is_sel else 0.16))
                                if _is_sel:
                                    add _pk_icon("check", "#ffffff") align (0.5, 0.5)

                null height 8

        use pk_scrollmark("ng_vp", _ng_accent, _ng_body_y, _ng_body_h)

        # ── Create button ──
        button:
            xpos PH_CX + 8
            ypos _ng_btn_y
            xsize _PK_CARD_W
            ysize _ng_btn_h
            sensitive _can_create
            padding (0, 0)
            background _pk_pill((_ng_accent if _can_create else "#64748b"), (0.85 if _can_create else 0.16))
            hover_background _pk_pill("#c4b5fd", 0.95)
            action [Hide("phone_create_group_screen"), Function(_phone_finalize_group, _selected_gids)]
            text _("Create Group"):
                style "phone_text"
                size 20
                bold True
                color ("#0f172a" if _can_create else _PK_DIM)
                xalign 0.5
                yalign 0.5

        use phone_chin_buttons(
            back_action=[Hide("phone_create_group_screen"), Show("phone_contacts_screen")])

# ============================================================
# GROUP CREATION FLOW
# ============================================================

label phone_create_group_flow:
    call screen phone_create_group_screen()

    if not isinstance(_return, list):
        # User cancelled via Back or Home — re-show contacts in this context
        # Use renpy.show_screen so it persists after call_in_new_context returns
        $ renpy.show_screen("phone_contacts_screen")
        return

    # _return is a list of selected gids
    python:
        _sel_gids = _return
        _names = [_girl_name_by_gid(g) for g in _sel_gids]
        _group_name = " & ".join(_names[:3])
        if len(_names) > 3:
            _group_name += " +%d" % (len(_names) - 3)
        _new_gid = phone_create_group(_group_name, _sel_gids)
        _new_group = None
        for _pg in phone_get_groups():
            if _pg["id"] == _new_gid:
                _new_group = _pg
                break
        phone_group_add_msg(_new_gid, "player", _tl(_("Group created!")), "system")
        # Girls react to being added
        _group_creation_reactions(_new_gid, _sel_gids)

    if _new_group is not None:
        call phone_open_group_chat(_new_group) from _call_phone_open_group_chat
    else:
        show screen phone_contacts_screen()
    return

# ============================================================
# Helper: open a newly created group (called via call_in_new_context)
# ============================================================

label _phone_open_new_group:
    $ _new_grp = store._pending_new_group
    call phone_open_group_chat(_new_grp) from _call_phone_open_new_group
    return

# ============================================================
# GROUP CHAT FLOW (placeholder)
# ============================================================

label phone_open_group_chat(group):
    $ _phone_hide_others()
    $ _check_group_friendship_updates(group["id"], group["members"])

    label .gchat_loop:
        call screen phone_group_chat_screen(group)
        $ print("[GCHAT_LOOP] _return=%s group=%s" % (repr(_return), group.get("id", "?")))

        # Remap partner_* actions to regular actions for multi-girl groups
        python:
            if _return in ("partner_invite", "partner_video"):
                _pm = group.get("members", [])
                _pg_count = sum(1 for m in _pm if not str(m).startswith("npc_"))
                if _pg_count >= 2:
                    _remap = {"partner_invite": "invite", "partner_video": "video"}
                    print("[GCHAT_LOOP] Remapped %s -> %s (multi-girl group, %d girls)" % (_return, _remap[_return], _pg_count))
                    _return = _remap[_return]

        if _return == "invite":
            python:
                _loc = store.CurrentLocation
                _loc_label = LOC_NAMES.get(_loc, _loc)

                _GROUP_INVITE_MSGS = {
                    "campus":    _tl(_("Hey girls, want to hang out at the campus with me?")),
                    "pool":      _tl(_("Hey, do you want to join me at the pool?")),
                    "showers":   _tl(_("I'm at the showers, wanna come?")),
                    "room":      _tl(_("Hey, want to come to my room?")),
                    "gwen_room": _tl(_("I'm in Gwen's room, come hang out!")),
                    "rogue_room":_tl(_("I'm in Rogue's room, come hang out!")),
                    "classroom": _tl(_("I'm at the classroom, want to join?")),
                    "gym":       _tl(_("Hey, I'm at the gym. Wanna work out together?")),
                    "mall":      _tl(_("Hey, I'm at the mall. Wanna come hang out?")),
                }
                _invite_msg = _GROUP_INVITE_MSGS.get(_loc, _tl(_("Hey, want to come hang out with me at %s?")) % _loc_label)
                phone_group_add_msg(group["id"], "player", _invite_msg, "text")

                _ALREADY_HERE = [
                    _("I'm already here, silly!"),
                    _("Haha, I'm right here!"),
                    _("Look around... I'm already here~"),
                    _("Already here! Did you not see me?"),
                ]

                # Build list of (gid, response_text, system_text_or_None, move_girl)
                _invite_replies = []
                _invite_npc = None
                _invite_girl_accepts = {}
                for _gid in group["members"]:
                    if str(_gid).startswith("npc_"):
                        _invite_npc = NPC_PARTNERS.get(_gid)
                        continue
                    _g = GIRL_BY_ID.get(_gid)
                    if _g is None:
                        continue
                    if getattr(_g, "loc", None) == _loc:
                        _invite_replies.append((_gid, _tl(renpy.random.choice(_ALREADY_HERE)), None, False))
                        _invite_girl_accepts[_gid] = True
                    else:
                        _fi_result, _fi_reason = _girl_accepts_invite(_g)
                        if _fi_result:
                            _invite_replies.append((_gid, _tl(renpy.random.choice(_PHONE_INVITE_ACCEPT)), _tl(_("%s is on her way.")) % _g.Name, True))
                            _invite_girl_accepts[_gid] = True
                        else:
                            _fi_pool = FOLLOW_INVITE_DECLINE.get(_fi_reason, _PHONE_INVITE_DECLINE)
                            _fi_raw = renpy.random.choice(_fi_pool)
                            if _fi_reason in _FOLLOW_DECLINE_PARTNER_FMT:
                                _fi_dec = _format_partner_line(_g, _fi_raw)
                            else:
                                _fi_dec = _tl(_fi_raw)
                            _invite_replies.append((_gid, _fi_dec, None, False))
                            _invite_girl_accepts[_gid] = False
                # NPC tags along if his GF is coming
                if _invite_npc is not None:
                    _npc_gf_gid = getattr(_invite_npc, "girl_gid", None)
                    _npc_gf_coming = _invite_girl_accepts.get(_npc_gf_gid, False)
                    if _npc_gf_coming:
                        _npc_gf_obj = GIRL_BY_ID.get(_npc_gf_gid)
                        _npc_already = getattr(_invite_npc, "loc", None) == _loc
                        if _npc_already:
                            _npc_line = _tl(renpy.random.choice(PARTNER_ALREADY_HERE_NPC_LINES))
                        else:
                            _npc_raw = _tl(renpy.random.choice(PARTNER_INVITE_NPC_LINES[_partner_npc_friend_key(_invite_npc)]))
                            _npc_line = _format_npc_line(_invite_npc, _npc_raw, _npc_gf_obj)
                        _invite_replies.append((_invite_npc.gid, _npc_line, None, not _npc_already))

            # Show typing + reply for each girl
            $ _inv_idx = 0
            while _inv_idx < len(_invite_replies):
                $ _inv_gid, _inv_text, _inv_sys, _inv_move = _invite_replies[_inv_idx]
                if not _phone_ctrl_held():
                    # Show typing indicator
                    $ phone_group_add_msg(group["id"], _inv_gid, None, "typing")
                    $ _inv_delay = renpy.random.uniform(0.8, 1.4)
                    call screen phone_group_chat_screen(group, auto_close=_inv_delay)
                    # Remove typing
                    python:
                        _g_msgs = phone_group_get_msgs(group["id"])
                        if _g_msgs and _g_msgs[-1].get("type") == "typing":
                            _g_msgs.pop()
                # Add real message
                python:
                    phone_group_add_msg(group["id"], _inv_gid, _inv_text, "text")
                    if _inv_sys:
                        phone_group_add_msg(group["id"], "system", _inv_sys, "system")
                    if _inv_move:
                        _mg = GIRL_BY_ID.get(_inv_gid)
                        _mn = NPC_PARTNERS.get(_inv_gid) if _mg is None else None
                        if _mg:
                            _mg.loc = _loc
                            _girls_now = [_g for _g in ALL_GIRLS if _g.loc == _loc]
                            _npc_here = getattr(store, "_npc_on_scene", None)
                            build_location_roster(_girls_now, _npc_here)
                            _sprite_suppressed.discard(_mg.Id)
                            show_roster_sprites()
                            if not hasattr(store, "_phone_girls_arrived"):
                                store._phone_girls_arrived = []
                            store._phone_girls_arrived.append(_mg.gid)
                        elif _mn:
                            _mn.loc = _loc
                            _girls_now = [_g for _g in ALL_GIRLS if _g.loc == _loc]
                            build_location_roster(_girls_now, _mn)
                            show_roster_sprites()
                    _inv_idx += 1
                # Brief pause to show the message before next girl types
                if not _phone_ctrl_held():
                    call screen phone_group_chat_screen(group, auto_close=0.4)

            jump .gchat_loop

        if _return == "video":
            python:
                _vids = getattr(store.Player, "recorded_videos", [])
            if not _vids:
                $ phone_group_add_msg(group["id"], "system", _("You don't have any recorded videos."), "system")
                jump .gchat_loop

            # Step 1: Pick girl from videos
            python:
                _girl_gids = sorted(set(v["girl_gid"] for v in _vids))
                _vid_girl_choices = []
                for _gid in _girl_gids:
                    _cg = GIRL_BY_ID.get(_gid)
                    if _cg:
                        _vid_girl_choices.append((_cg.Name, _gid))
            call screen phone_group_chat_screen(group, choices=_vid_girl_choices)
            $ _chosen_gid = _return
            if _chosen_gid in ("home", None):
                jump .gchat_loop
            if _chosen_gid == "close":
                jump .gchat_loop

            # Step 2: Pick position (split by consent/face_hidden)
            python:
                _gid_vids_g = [v for v in _vids if v["girl_gid"] == _chosen_gid]
                _combos_g = set()
                for _cv in _gid_vids_g:
                    if _cv.get("special"):
                        continue
                    _var = "nc" if not _cv.get("consensual", True) else ("h" if _cv.get("face_hidden", True) else "v")
                    _combos_g.add((_cv["type"], _var))
                _combos_g = sorted(_combos_g)
                _vid_pos_choices = []
                for _pos, _var in _combos_g:
                    _label = _pk_t(VIDEO_TYPE_DISPLAY.get(_pos, _pos.replace("_", " ").title()))
                    if _var == "nc":
                        _label += " {size=18}(" + _tl(_("non-consensual")) + "){/size}"
                    elif _var == "h":
                        _label += " {size=18}(" + _tl(_("hidden face")) + "){/size}"
                    else:
                        _label += " {size=18}(" + _("face visible") + "){/size}"
                    _vid_pos_choices.append((_label, _pos + "|" + _var))
                _has_special_g = any(v.get("special") for v in _gid_vids_g)
                if _has_special_g:
                    _vid_pos_choices.append((_("SPECIAL"), "special"))
            call screen phone_group_chat_screen(group, choices=_vid_pos_choices)
            $ _chosen_pos = _return
            if _chosen_pos in ("home", "close", None):
                jump .gchat_loop

            # Parse variant from choice value
            python:
                _chosen_face_hidden = None
                _chosen_nonconsensual = False
                if _chosen_pos and "|" in str(_chosen_pos):
                    _pparts = _chosen_pos.split("|")
                    _chosen_pos = _pparts[0]
                    if _pparts[1] == "nc":
                        _chosen_nonconsensual = True
                    elif _pparts[1] == "h":
                        _chosen_face_hidden = True
                    else:
                        _chosen_face_hidden = False

            # Step 2b: If SPECIAL, pick the specific special type
            if _chosen_pos == "special":
                python:
                    _special_types_g = sorted(set(v.get("special") for v in _gid_vids_g if v.get("special")))
                    _special_choices_g = [(SPECIAL_VIDEO_DISPLAY.get(s, s.title()), s) for s in _special_types_g]
                call screen phone_group_chat_screen(group, choices=_special_choices_g)
                $ _chosen_special_g = _return
                if _chosen_special_g in ("home", "close", None):
                    jump .gchat_loop

            # Step 3: Pick location (if multiple)
            python:
                if _chosen_pos == "special":
                    _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v.get("special") == _chosen_special_g]
                elif _chosen_nonconsensual:
                    _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v["type"] == _chosen_pos and not v.get("special") and not v.get("consensual", True)]
                else:
                    _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v["type"] == _chosen_pos and not v.get("special") and v.get("consensual", True)]
                    if _chosen_face_hidden is not None:
                        _matching = [v for v in _matching if v.get("face_hidden", True) == _chosen_face_hidden]
                _locs = sorted(set(v.get("location", "unknown") for v in _matching))
            if len(_locs) > 1:
                python:
                    _VID_LOC_NAMES = {
                        "campus": _tr("Campus"), "pool": _tr("Pool"), "showers": _tr("Showers"), "apartment": _tr("Apartment"), "apartment_room": _tr("Apartment Bedroom"), "apartment_shower": _tr("Apartment Bathroom"),
                        "room": _tr("%s's Room") % store.Player.Name,
                        "gwen_room": _tr("Gwen's Room"), "rogue_room": _tr("Rogue's Room"), "ntw_room": _tr("Negasonic's Room"), "tenny_room": _tr("%s's Room") % GIRL_BY_ID["tenny"].Name,
                        "classroom": _tr("Classroom"), "gym": _tr("Gym"), "hall": _tr("Hall"),
                        "street": _tr("Street"), "mall": _tr("Mall"), "party": _tr("Party"),
                    }
                    _vid_loc_choices = [(_VID_LOC_NAMES.get(l, l.replace("_", " ").title()), l) for l in _locs]
                call screen phone_group_chat_screen(group, choices=_vid_loc_choices)
                $ _chosen_loc = _return
                if _chosen_loc in ("home", "close", None):
                    jump .gchat_loop
            else:
                $ _chosen_loc = _locs[0] if _locs else None

            if _chosen_loc in (None, "close"):
                jump .gchat_loop

            # Step 4: Condom choice (only for RCG/cowgirl when both versions exist)
            python:
                _loc_vids = [v for v in _matching if v.get("location", "") == _chosen_loc]
                _has_condom = any(v.get("condom", False) for v in _loc_vids)
                _has_raw = any(v.get("condom") == False and "condom" in v for v in _loc_vids)
                _show_condom_choice = _chosen_pos in (_("cowgirl"), "reverse_cowgirl") and _has_condom and _has_raw
                _chosen_condom = None
            if _show_condom_choice:
                call screen phone_group_chat_screen(group, choices=[("Condom", True), ("Raw", False)])
                $ _chosen_condom = _return
                if _chosen_condom in ("home", "close", None):
                    jump .gchat_loop

            # Resolve the video
            python:
                _sent_vid = None
                for _v in reversed(_loc_vids if _loc_vids else _matching):
                    if _v.get("location", "") == _chosen_loc:
                        if _show_condom_choice:
                            if _v.get("condom") == _chosen_condom:
                                _sent_vid = _v
                                break
                        else:
                            _sent_vid = _v
                            break
                if _sent_vid is None:
                    _sent_vid = _matching[-1] if _matching else {"girl_gid": _chosen_gid, "type": _chosen_pos, "location": _chosen_loc, "consensual": True}
                _vid_girl = GIRL_BY_ID.get(_chosen_gid)
                _vid_name = _vid_girl.Name if _vid_girl else "someone"
                _vid_loc = _sent_vid.get("location", "room") if _sent_vid else "room"
                _vid_loc_names = {
                    "room": _("in your room"), "campus": _("on campus"), "pool": _("at the pool"),
                    "hall": _("in the hallway"), "street": _("on the street"), "mall": _("at the mall"),
                    "party": _("at the party"), "gym": _("at the gym"), "classroom": _("in the classroom"),
                    "showers": _("in the showers"), "apartment": _("in the apartment"), "apartment_room": _("in the bedroom"), "apartment_shower": _("in the bathroom"), "shower": _("in the shower"), "bathroom": _("in the bathroom"),
                    "library": _("in the library"), "dorm": _("in the dorm"), "kitchen": _("in the kitchen"),
                    "park": _("at the park"), "beach": _("at the beach"), "car": _("in the car"),
                    "office": _("in the office"), "rooftop": _("on the rooftop"),
                    "gwen_room": _("in a dorm room"), "rogue_room": _("in a dorm room"), "ntw_room": _("in a dorm room"),
                }
                if _vid_loc == _chosen_gid + "_room":
                    _vid_loc_names[_vid_loc] = _("in her room")
                _vid_loc_str = _tl(_vid_loc_names.get(_vid_loc, _vid_loc.replace("_", " ")))
                _vid_send_descs = {
                    "hj": _("You sent a video of %s jerking you off %s"),
                    "bj": _("You sent a video of %s sucking your dick %s"),
                    "tj": _("You sent a video of %s's tits wrapped around your dick %s"),
                    "cowgirl": _("You sent a video of %s riding you %s"),
                    "reverse_cowgirl": _("You sent a video of %s riding you facing away %s"),
                    "creampie": _("You sent a video of you cumming inside %s %s"),
                    "masturbate": _("You sent a video of %s touching herself %s"),
                    "sex": _("You sent a video of you fucking %s %s"),
                    "anal": _("You sent a video of you doing anal with %s %s"),
                    "laying_down": _("You sent a video of you on top of %s %s"),
                    "laying_anal": _("You sent a video of you doing anal with %s while on top %s"),
                    "reverse_cowgirl_anal": _("You sent a video of %s riding you in reverse with it in her ass %s"),
                }
                _vid_send_msg = _tl(_vid_send_descs.get(_chosen_pos, _("You sent a video of %s %s"))) % (_vid_name, _vid_loc_str)
                phone_group_add_msg(group["id"], "player", _vid_send_msg, "system")

            # Each girl reacts with typing dots
            python:
                # ── Priority 0: GF cheating breakup (overrides scripted convos) ──
                _gv_gf_breakup = False
                _vid_was_ex = _vid_snap(_sent_vid, "was_dating", False)
                _vid_gid = _sent_vid.get("girl_gid", "")
                for _gv_gid_chk in group.get("members", []):
                    _gv_gf_chk = GIRL_BY_ID.get(_gv_gid_chk)
                    if _gv_gf_chk is None or girl_is_away(_gv_gf_chk):
                        continue
                    _is_dat = hasattr(_gv_gf_chk, "is_dating_player") and _gv_gf_chk.is_dating_player()
                    _is_other = _vid_gid != _gv_gf_chk.gid
                    if _is_dat and _is_other and not _vid_was_ex:
                        _harem = getattr(_gv_gf_chk, "harem_accepted", set()) or set()
                        _is_poly = hasattr(_gv_gf_chk, "has_trait") and _gv_gf_chk.has_trait("polyamorous")
                        _is_harem_ok = _vid_gid in _harem
                        if not _is_poly and not _is_harem_ok:
                            _gv_gf_breakup = True
                            break

                if _gv_gf_breakup:
                    # GF breakup overrides scripted convos — run normal per-girl reactions
                    # which will hit the breakup gate in group_video_reaction()
                    _gv_all_reactions = []
                    _gv_is_scripted = False
                    store._gv_virgin_shock_covered = set()
                    store._group_used_lines = set()
                    for _gv_gid in group["members"]:
                        if _gv_gid in store._gv_virgin_shock_covered:
                            continue
                        _gv_girl = GIRL_BY_ID.get(_gv_gid)
                        if _gv_girl is None:
                            continue
                        store._phone_msg_queue = []
                        _phone_mode_on(_gv_girl)
                        try:
                            group_video_reaction(_gv_girl, _sent_vid, group)
                        finally:
                            _phone_mode_off()
                        for _qm in store._phone_msg_queue:
                            _gv_all_reactions.append((_qm.get("sender", _gv_gid), _qm["text"]))
                        store._phone_msg_queue = []
                    store._gv_virgin_shock_covered = set()
                    store._group_used_lines = None
                else:
                    # Check for scripted multi-message conversations first
                    _gv_all_reactions = _try_scripted_group_video(_sent_vid, group)
                    _gv_is_scripted = _gv_all_reactions is not None

                if not _gv_gf_breakup and not _gv_is_scripted:
                    # Normal per-girl reactions
                    _gv_all_reactions = []
                    # Track girls already covered by another girl's virgin shock convo
                    store._gv_virgin_shock_covered = set()
                    store._group_used_lines = set()
                    for _gv_gid in group["members"]:
                        if _gv_gid in store._gv_virgin_shock_covered:
                            continue
                        _gv_girl = GIRL_BY_ID.get(_gv_gid)
                        if _gv_girl is None:
                            continue
                        store._phone_msg_queue = []
                        _phone_mode_on(_gv_girl)
                        try:
                            group_video_reaction(_gv_girl, _sent_vid, group)
                        finally:
                            _phone_mode_off()
                        for _qm in store._phone_msg_queue:
                            _gv_all_reactions.append((_qm.get("sender", _gv_gid), _qm["text"]))
                        store._phone_msg_queue = []
                    store._gv_virgin_shock_covered = set()
                    store._group_used_lines = None

            # NPC reaction in mixed groups (partner_video routed here)
            python:
                if not _gv_is_scripted:
                    for _gv_npc_gid in group.get("members", []):
                        if not str(_gv_npc_gid).startswith("npc_"):
                            continue
                        _gv_npc = NPC_PARTNERS.get(_gv_npc_gid)
                        if _gv_npc is None:
                            continue
                        _gv_npc_line = _npc_video_reaction(_gv_npc, _sent_vid, girl_present=(getattr(_gv_npc, "girl_gid", None) in group.get("members", [])))
                        if _gv_npc_line:
                            _gv_all_reactions.append((_gv_npc_gid, _gv_npc_line))
                        if getattr(_gv_npc, "_ntr_active", False) and hasattr(_gv_npc, "is_hostile") and _gv_npc.is_hostile():
                            _gv_npc_gf = GIRL_BY_ID.get(getattr(_gv_npc, "girl_gid", ""))
                            if _gv_npc_gf:
                                _gf_will_taunt = getattr(_gv_npc_gf, "CheatAttitude", 1) >= 6 or (hasattr(_gv_npc_gf, "has_trait") and _gv_npc_gf.has_trait("cheater"))
                                _gf_is_loyal = hasattr(_gv_npc_gf, "has_trait") and _gv_npc_gf.has_trait("loyal")
                                if _gf_will_taunt and not _gf_is_loyal:
                                    _gv_reinforce = _format_partner_line(_gv_npc_gf, _tl(renpy.random.choice(PARTNER_VIDEO_GIRL_REINFORCE)))
                                    _gv_all_reactions.append((_gv_npc_gf.gid, _gv_reinforce))

            # Replay each reaction with typing
            $ _gv_ri = 0
            while _gv_ri < len(_gv_all_reactions):
                $ _gvr_gid, _gvr_text = _gv_all_reactions[_gv_ri]
                if not _phone_ctrl_held():
                    # Show typing indicator
                    $ phone_group_add_msg(group["id"], _gvr_gid, None, "typing")
                    if _gv_is_scripted:
                        $ _gvr_delay = renpy.random.uniform(1.8, 2.8)
                    else:
                        $ _gvr_delay = renpy.random.uniform(0.8, 1.4)
                    call screen phone_group_chat_screen(group, auto_close=_gvr_delay)
                    # Remove typing
                    python:
                        _g_msgs = phone_group_get_msgs(group["id"])
                        if _g_msgs and _g_msgs[-1].get("type") == "typing":
                            _g_msgs.pop()
                # Add real message
                python:
                    phone_group_add_msg(group["id"], _gvr_gid, _gvr_text, "text")
                    _gv_ri += 1
                # Brief pause before next message
                if not _phone_ctrl_held():
                    if _gv_is_scripted:
                        call screen phone_group_chat_screen(group, auto_close=0.8)
                    else:
                        call screen phone_group_chat_screen(group, auto_close=0.4)

            # NPC dissolution check (boundary violation / video pending)
            python:
                _gv_npc_dissolve = False
                _gv_leaving_npc = None
                for _gv_dc_gid in group.get("members", []):
                    if not str(_gv_dc_gid).startswith("npc_"):
                        continue
                    _gv_dc_npc = NPC_PARTNERS.get(_gv_dc_gid)
                    if _gv_dc_npc is None:
                        continue
                    _gv_dc_gf = GIRL_BY_ID.get(getattr(_gv_dc_npc, "girl_gid", ""))
                    if _gv_dc_gf and (getattr(_gv_dc_gf, "_npc_video_pending", False) or getattr(_gv_dc_gf, "_ntr_violation_pending", False)):
                        _gv_dc_gf._partner_confront_pending = True
                        _gv_npc_dissolve = True
                        _gv_leaving_npc = _gv_dc_npc
            if _gv_npc_dissolve:
                # Bystander + GF reactions
                python:
                    _gv_dissolve_reactions = _group_dissolve_reactions(group, _gv_leaving_npc)
                $ _gv_dr_i = 0
                while _gv_dr_i < len(_gv_dissolve_reactions):
                    $ _gv_dr_gid, _gv_dr_text = _gv_dissolve_reactions[_gv_dr_i]
                    if not _phone_ctrl_held():
                        $ phone_group_add_msg(group["id"], _gv_dr_gid, None, "typing")
                        call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
                        python:
                            _g_msgs = phone_group_get_msgs(group["id"])
                            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                                _g_msgs.pop()
                    python:
                        phone_group_add_msg(group["id"], _gv_dr_gid, _gv_dr_text, "text")
                        _gv_dr_i += 1
                    if not _phone_ctrl_held():
                        call screen phone_group_chat_screen(group, auto_close=0.5)

                # NPC leaves
                $ phone_group_add_msg(group["id"], "system", _tl(_("%s left the group.")) % _gv_leaving_npc.Name, "system")
                if not _phone_ctrl_held():
                    call screen phone_group_chat_screen(group, auto_close=0.8)

                # All other members leave and group is deleted
                python:
                    for _gv_lv_gid in list(group.get("members", [])):
                        if str(_gv_lv_gid).startswith("npc_"):
                            continue
                        _gv_lv_girl = GIRL_BY_ID.get(_gv_lv_gid)
                        if _gv_lv_girl:
                            phone_group_add_msg(group["id"], "system", _tl(_("%s left the group.")) % _gv_lv_girl.Name, "system")
                call screen phone_group_chat_screen(group)
                python:
                    _pgs = getattr(store.Player, "phone_groups", [])
                    store.Player.phone_groups = [g for g in _pgs if g.get("id") != group["id"]]
                    _phone_restore_others()
                return

            jump .gchat_loop

        if _return == "group_delete":
            # Tidying duplicate groups (tester 2026-10-10): the group and its history go for good, after
            # a confirm inside the chat. The harem group has no tile for this (the harem system owns it).
            call screen phone_group_chat_screen(group, choices=[
                (_tl(_("Delete the group, history included")), "group_delete_yes"),
                (_tl(_("Keep the group")), "group_delete_no")])
            if _return == "group_delete_yes":
                python:
                    phone_group_delete(group["id"])
                    _phone_restore_others()
                return
            jump .gchat_loop

        if _return == "dinner_group":
            call restaurant_send_group_invite(group) from _call_rest_group_invite
            jump .gchat_loop

        if _return == "hangout":
            $ print("[GCHAT_LOOP] MATCHED hangout, calling hangout_send_invite")
            call hangout_send_invite(group) from _call_hangout_send_invite
            jump .gchat_loop

        if _return == "partner_invite":
            call _partner_group_invite(group) from _call_partner_group_invite
            jump .gchat_loop

        if _return == "partner_video":
            call _partner_group_send_video(group) from _call_partner_group_send_video
            if getattr(store, "_partner_group_dissolved", False):
                $ store._partner_group_dissolved = False
                $ _phone_restore_others()
                return
            jump .gchat_loop

        if _return == "partner_hangout":
            python:
                _pm = group.get("members", [])
                _pg_count = sum(1 for m in _pm if not str(m).startswith("npc_"))
            if _pg_count >= 2:
                $ print("[GCHAT_LOOP] MATCHED partner_hangout (multi-girl), routing to hangout_send_invite")
                call hangout_send_invite(group) from _call_hangout_send_invite_mixed
            else:
                $ print("[GCHAT_LOOP] MATCHED partner_hangout, calling hangout_send_invite_partner")
                call hangout_send_invite_partner(group) from _call_hangout_send_invite_partner
            jump .gchat_loop

        if _return == "group_dick_pic":
            # Process each girl independently
            python:
                _gdp_results = []
                for _gdp_gid in group["members"]:
                    _gdp_girl = GIRL_BY_ID.get(_gdp_gid)
                    if _gdp_girl is None:
                        continue
                    _gdp_r = _dp_process_dickpic(_gdp_girl)
                    if _gdp_r is not None:
                        _gdp_results.append((_gdp_gid, _gdp_r))

            if not _gdp_results:
                $ phone_group_add_msg(group["id"], "system", _tl(_("You already sent one today. Give them some time.")), "system")
                jump .gchat_loop

            $ phone_group_add_msg(group["id"], "player", _tl(_("You sent a photo.")), "system")
            if not _phone_ctrl_held():
                call screen phone_group_chat_screen(group, auto_close=0.3)

            python:
                _gdp_idx = 0
            while _gdp_idx < len(_gdp_results):
                python:
                    _gdp_gid, _gdp_r = _gdp_results[_gdp_idx]
                if not _phone_ctrl_held():
                    # Typing indicator
                    $ phone_group_add_msg(group["id"], _gdp_gid, None, "typing")
                    $ _gdp_delay = renpy.random.uniform(0.8, 1.4)
                    call screen phone_group_chat_screen(group, auto_close=_gdp_delay)
                    python:
                        _g_msgs = phone_group_get_msgs(group["id"])
                        if _g_msgs and _g_msgs[-1].get("type") == "typing":
                            _g_msgs.pop()
                python:
                    phone_group_add_msg(group["id"], _gdp_gid, _gdp_r["line"], "text")
                    _gdp_idx += 1
                if not _phone_ctrl_held():
                    call screen phone_group_chat_screen(group, auto_close=0.4)

            jump .gchat_loop

        if _return == "propose_member":
            call _harem_propose_member(group) from _call_harem_propose
            jump .gchat_loop

        if _return == "group_dinner":
            call restaurant_send_group_invite(group) from _call_rest_group_invite_harem
            jump .gchat_loop

    $ print("[PHONE_GROUP] exiting group chat, _return=%s" % repr(_return))
    $ _phone_restore_others()
    return


# ============================================================
# HAREM ACCEPTANCE PHONE EVENT — morning after GF catches player
# ============================================================

label _harem_ask_phone_event(girl):

    python:
        _harem_caught_gid = getattr(girl, "_harem_caught_with_gid", None)
        _harem_caught_act = getattr(girl, "_harem_caught_act", "sex")
        _harem_other = GIRL_BY_ID.get(_harem_caught_gid) if _harem_caught_gid else None
        _harem_other_name = _harem_other.Name if _harem_other else "her"
        _harem_suggests = getattr(girl, "_harem_caught_suggests_add", False)
        print("[HAREM_PHONE] Event for %s, caught with %s (%s), suggests_add=%s" % (girl.gid, _harem_caught_gid, _harem_caught_act, _harem_suggests))

    if _harem_other is None:
        $ girl._harem_ask_pending = False
        return

    # Route: group notification vs 1-on-1 phone
    python:
        _hpe_hg = _get_harem_group()
        _hpe_girl_in_group = _hpe_hg is not None and girl.gid in _hpe_hg.get("members", [])

    if _hpe_girl_in_group:
        call _harem_caught_group_notify(girl) from _call_harem_caught_grp
        return

    # ── 1-on-1 phone flow (no harem group yet) ──

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. A message from [girl.Name]. She wants to talk about yesterday."

    python:
        _harem_open_lines = {
            "polyamorous": [
                _("Hey. So... yesterday happened. I'm not going to pretend I wasn't surprised."),
                _("Look, I knew what I was getting into with you. But seeing it was... different."),
            ],
            "monogamous": [
                _("I barely slept last night. I keep replaying what I saw in my head."),
                _("I need to talk about yesterday. I'm still shaking just thinking about it."),
            ],
            "cute_sex": [
                _("I cried a little last night, not going to lie... but I also couldn't stop thinking about you."),
                _("Yesterday really hurt... but I don't want to lose you over it..."),
            ],
            "hardcore_sex": [
                _("So. Yesterday. We need to address the elephant in the room."),
                _("I'm not going to sugarcoat it. Yesterday pissed me off. But I'm still here."),
            ],
            "_default": [
                _("About yesterday... I've been thinking a lot. We need to talk."),
                _("I saw what I saw. I'm not going to pretend it didn't happen. Can we talk?"),
            ],
        }
        _open_line = None
        for _t in ("polyamorous", "monogamous", "cute_sex", "hardcore_sex"):
            if girl.has_trait(_t):
                _open_line = renpy.random.choice(_harem_open_lines[_t])
                break
        if _open_line is None:
            _open_line = renpy.random.choice(_harem_open_lines["_default"])

    call _phone_typing(girl) from _call_harem_phone_typing_1
    $ phone_add_msg(girl.gid, girl.gid, _open_line)
    call screen phone_chat_screen(girl, auto_close=1.2, choices=[])

    python:
        _harem_open2 = _tl(_("You and %s... I saw everything. And I didn't leave.")) % _harem_other_name

    call _phone_typing(girl) from _call_harem_phone_typing_2
    $ phone_add_msg(girl.gid, girl.gid, _harem_open2)
    call screen phone_chat_screen(girl, auto_close=0, choices=[])

    python:
        _harem_choices = [
            (_("Ask her about sharing"), "ask_share"),
            (_("Tell her it was a mistake"), "decline"),
        ]

    call screen phone_chat_screen(girl, choices=_harem_choices, can_leave=True)
    $ _harem_player_choice = _return

    if _harem_player_choice == "ask_share":
        $ phone_add_msg(girl.gid, "player", _tl(_("I know this is a lot to ask... but would you be open to sharing? To all of us being together?")))
        call screen phone_chat_screen(girl, auto_close=0.8, choices=[])

        python:
            _harem_accept_lines = {
                "polyamorous": [
                    _("Honestly? I've thought about it before. I'm not wired for jealousy the way most people are. Let's try it."),
                    _("I'm in. Life's too short to put limits on love. Just... be honest with me, always."),
                ],
                "monogamous": [
                    _("I can't believe I'm saying this... Every part of me screams no. But I love you too much to walk away. Fine. I'll try."),
                    _("This is the hardest thing I've ever agreed to. Don't make me regret it."),
                ],
                "cute_sex": [
                    _("I'm scared... really scared. But if it means keeping you in my life... I'll try to be okay with it."),
                    _("My heart screams no, but I also know I can't lose you... so... okay. I'll try."),
                ],
                "hardcore_sex": [
                    _("You've got balls asking me this. But fine. Just know that if I'm sharing, I expect to be the priority."),
                    _("Whatever. As long as you don't forget who was here first. Deal?"),
                ],
                "_default": [
                    _("That's... a big ask. But I didn't leave yesterday for a reason. Okay. Let's see how this goes."),
                    _("I won't pretend this is normal for me. But I'd rather be part of your life like this than not at all."),
                ],
            }
            _acc_line = None
            for _t in ("polyamorous", "monogamous", "cute_sex", "hardcore_sex"):
                if girl.has_trait(_t):
                    _acc_line = renpy.random.choice(_harem_accept_lines[_t])
                    break
            if _acc_line is None:
                _acc_line = renpy.random.choice(_harem_accept_lines["_default"])

        call _phone_typing(girl) from _call_harem_phone_typing_3
        $ phone_add_msg(girl.gid, girl.gid, _acc_line)
        call screen phone_chat_screen(girl, auto_close=0, choices=[])

        # Finalize harem + create/join group
        python:
            girl._open_relationship_consent = True
            add_to_harem(girl, _harem_caught_gid)
            if _harem_other and _harem_other.is_dating_player():
                add_to_harem(_harem_other, girl.gid)

            _hg = _get_harem_group()
            if _hg is None:
                _create_harem_group(girl)
                _hg = _get_harem_group()
                phone_group_add_msg(_hg["id"], "system", _tl(_("%s opened the relationship.")) % girl.Name, "system")
            elif girl.gid not in _hg["members"]:
                _hg["members"].append(girl.gid)
                phone_group_add_msg(_hg["id"], "system", _tl(_("%s joined the group.")) % girl.Name, "system")

            if _harem_other and _harem_other.gid not in _hg["members"]:
                _harem_other._open_relationship_consent = True
                _hg["members"].append(_harem_other.gid)
                phone_group_add_msg(_hg["id"], "system", _tl(_("%s joined the group.")) % _harem_other.Name, "system")

            print("[HAREM_PHONE] %s accepted sharing with %s. Group=%s" % (girl.gid, _harem_caught_gid, _hg["id"]))

        "You put the phone down. This changes everything."

    else:
        $ phone_add_msg(girl.gid, "player", _tl(_("I'm sorry. Yesterday was a mistake. It won't happen again.")))
        call screen phone_chat_screen(girl, auto_close=0.8, choices=[])

        python:
            _harem_decline_lines = {
                "polyamorous": [
                    _("A mistake? Hm. I wouldn't have minded, you know. But okay. Your call."),
                    _("If you say so. Just know the door was open on my end."),
                ],
                "cute_sex": [
                    _("...Thank you for saying that. I really needed to hear it. Please don't do it again."),
                    _("I want to believe you... I really do. Just... please keep that promise."),
                ],
                "hardcore_sex": [
                    _("It better not. I'm not the forgiving type. You got ONE pass."),
                    _("Fine. But if it happens again, we're done. No second chances."),
                ],
                "_default": [
                    _("Okay. I'm choosing to trust you. Don't make me regret it."),
                    _("I hope you mean that. Because I'm giving you another chance."),
                ],
            }
            _dec_line = None
            for _t in ("polyamorous", "cute_sex", "hardcore_sex"):
                if girl.has_trait(_t):
                    _dec_line = renpy.random.choice(_harem_decline_lines[_t])
                    break
            if _dec_line is None:
                _dec_line = renpy.random.choice(_harem_decline_lines["_default"])

        call _phone_typing(girl) from _call_harem_phone_typing_4
        $ phone_add_msg(girl.gid, girl.gid, _dec_line)
        call screen phone_chat_screen(girl, auto_close=0, choices=[])

        $ Change_Status(girl, "Jealousy", 100, max_val=1000)
        "You put the phone down. Crisis averted, for now."

    # Clear pending flags
    python:
        girl._harem_ask_pending = False
        girl._harem_caught_with_gid = None
        girl._harem_caught_act = None
        girl._harem_caught_suggests_add = False

    return


# ============================================================
# HAREM CAUGHT — group notification (girl is already in harem group)
# ============================================================

label _harem_caught_group_notify(girl):

    python:
        _hcg_gid = getattr(girl, "_harem_caught_with_gid", None)
        _hcg_other = GIRL_BY_ID.get(_hcg_gid) if _hcg_gid else None
        _hcg_other_name = _hcg_other.Name if _hcg_other else "her"
        _hcg_suggests = getattr(girl, "_harem_caught_suggests_add", False)
        _hcg_group = _get_harem_group()
        print("[HAREM_GROUP_NOTIFY] %s posts about %s, suggests=%s" % (girl.gid, _hcg_gid, _hcg_suggests))

    if _hcg_group is None or _hcg_other is None:
        python:
            girl._harem_ask_pending = False
            girl._harem_caught_with_gid = None
            girl._harem_caught_act = None
            girl._harem_caught_suggests_add = False
        return

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. A new message in the group chat."

    # GF posts in the harem group
    if _hcg_suggests:
        # She likes the caught girl — suggest adding
        python:
            _hcg_suggest_lines = [
                _tl(_("So... I caught him with %s yesterday. I've been thinking about it, and honestly, I think she could fit in with us.")) % _hcg_other_name,
                _tl(_("I saw him with %s. Before anyone freaks out, I actually think we should talk about adding her to the group.")) % _hcg_other_name,
            ]
            _hcg_line = renpy.random.choice(_hcg_suggest_lines)

        $ phone_group_add_msg(_hcg_group["id"], girl.gid, None, "typing")
        $ _hcg_delay = renpy.random.uniform(1.2, 2.0)
        call screen phone_group_chat_screen(_hcg_group, auto_close=_hcg_delay)
        python:
            _g_msgs = phone_group_get_msgs(_hcg_group["id"])
            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                _g_msgs.pop()
            phone_group_add_msg(_hcg_group["id"], girl.gid, _hcg_line, "text")
        call screen phone_group_chat_screen(_hcg_group, auto_close=0.8)

        # Other members vote (excluding the GF who posted — she already accepts)
        python:
            # everybody votes: label Wait (6zy) never starts this event while a member is away (_harem_away_members)
            _hcg_other_voters = [gid for gid in _hcg_group["members"] if gid != girl.gid]
            _hcg_all_accept = True
            _hcg_rejector_gid = None
            _hcg_vote_results = []

            for _hcg_v_gid in _hcg_other_voters:
                _hcg_voter = GIRL_BY_ID.get(_hcg_v_gid)
                if _hcg_voter is None:
                    continue
                _hcg_vr, _hcg_vs, _hcg_vk = harem_vote_on_girl(_hcg_voter, _hcg_other)

                if _hcg_vr == "accept":
                    _hcg_vpool = {
                        "poly": [_("I'm fine with it. Let's do it.")],
                        "willing": [_("I think she'd be okay with us. Sure.")],
                        "likes_her": [_tl(_("I actually like %s. I'm in.")) % _hcg_other_name],
                        "forced": [
                            _("... Fine. Whatever you want."),
                            _("She can stay. Don't expect me to be nice about it."),
                        ],
                    }
                    _hcg_vline = renpy.random.choice(_hcg_vpool.get(_hcg_vk, _hcg_vpool["willing"]))
                    if _hcg_vk == "forced":
                        _hcg_fb = getattr(_hcg_voter, "_harem_forced_by", None)
                        if _hcg_fb is None:
                            _hcg_voter._harem_forced_by = set()
                            _hcg_fb = _hcg_voter._harem_forced_by
                        _hcg_fb.add(_hcg_other.gid)
                        print("[HAREM] %s forced to accept %s via caught-group vote" % (_hcg_voter.gid, _hcg_other.gid))
                else:
                    _hcg_vpool = {
                        "unwilling": [_("I'm not okay with this. I'm already at my limit.")],
                        "hostile": [_tl(_("No. I can't stand %s. Absolutely not.")) % _hcg_other_name],
                    }
                    _hcg_vline = renpy.random.choice(_hcg_vpool.get(_hcg_vk, _hcg_vpool["unwilling"]))
                    _hcg_all_accept = False
                    _hcg_rejector_gid = _hcg_v_gid

                _hcg_vote_results.append((_hcg_v_gid, _hcg_vr, _hcg_vline))
                if not _hcg_all_accept:
                    break

        # Replay votes with typing animation
        $ _hcg_vi = 0
        while _hcg_vi < len(_hcg_vote_results):
            python:
                _hcg_vr_gid, _hcg_vr_res, _hcg_vr_line = _hcg_vote_results[_hcg_vi]
            $ phone_group_add_msg(_hcg_group["id"], _hcg_vr_gid, None, "typing")
            $ _hcg_vd = renpy.random.uniform(1.0, 1.8)
            call screen phone_group_chat_screen(_hcg_group, auto_close=_hcg_vd)
            python:
                _g_msgs = phone_group_get_msgs(_hcg_group["id"])
                if _g_msgs and _g_msgs[-1].get("type") == "typing":
                    _g_msgs.pop()
                phone_group_add_msg(_hcg_group["id"], _hcg_vr_gid, _hcg_vr_line, "text")
            call screen phone_group_chat_screen(_hcg_group, auto_close=0.5)
            $ _hcg_vi += 1

        if _hcg_all_accept:
            python:
                phone_group_add_msg(_hcg_group["id"], "system", _tl(_("Everyone agreed! %s is now part of the group.")) % _hcg_other_name, "system")
                _hcg_group["members"].append(_hcg_other.gid)
                for _m_gid in _hcg_group["members"]:
                    if _m_gid != _hcg_other.gid:
                        _m_girl = GIRL_BY_ID.get(_m_gid)
                        if _m_girl:
                            add_to_harem(_m_girl, _hcg_other.gid)
                            add_to_harem(_hcg_other, _m_gid)
                _hcg_other._open_relationship_consent = True
                _store_group_tiers(_hcg_group["id"], _hcg_group["members"])
                print("[HAREM_GROUP_NOTIFY] %s added to harem via caught-suggest" % _hcg_other.gid)
            call screen phone_group_chat_screen(_hcg_group, auto_close=1.0)
        else:
            python:
                _rej_name = _girl_name_by_gid(_hcg_rejector_gid) if _hcg_rejector_gid else "Someone"
                phone_group_add_msg(_hcg_group["id"], "system", _tl(_("%s doesn't want %s in the group.")) % (_rej_name, _hcg_other_name), "system")
                print("[HAREM_GROUP_NOTIFY] %s rejected by %s" % (_hcg_other.gid, _hcg_rejector_gid))
            call screen phone_group_chat_screen(_hcg_group, auto_close=1.0)

    else:
        # She doesn't like the caught girl — tell player to stop
        python:
            _hcg_stop_lines = [
                _tl(_("I saw him with %s yesterday. I don't like her. He needs to stop seeing her.")) % _hcg_other_name,
                _tl(_("So %s is apparently in the picture now. I'm not okay with her. That's where I draw the line.")) % _hcg_other_name,
            ]
            _hcg_line = renpy.random.choice(_hcg_stop_lines)

        $ phone_group_add_msg(_hcg_group["id"], girl.gid, None, "typing")
        $ _hcg_delay = renpy.random.uniform(1.2, 2.0)
        call screen phone_group_chat_screen(_hcg_group, auto_close=_hcg_delay)
        python:
            _g_msgs = phone_group_get_msgs(_hcg_group["id"])
            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                _g_msgs.pop()
            phone_group_add_msg(_hcg_group["id"], girl.gid, _hcg_line, "text")
        call screen phone_group_chat_screen(_hcg_group, auto_close=0.8)

        python:
            phone_group_add_msg(_hcg_group["id"], "system", _tl(_("%s doesn't want %s in the group.")) % (girl.Name, _hcg_other_name), "system")
            print("[HAREM_GROUP_NOTIFY] %s says stop seeing %s" % (girl.gid, _hcg_other.gid))
        call screen phone_group_chat_screen(_hcg_group, auto_close=1.0)

    # Clear pending flags
    python:
        girl._harem_ask_pending = False
        girl._harem_caught_with_gid = None
        girl._harem_caught_act = None
        girl._harem_caught_suggests_add = False

    return

# ============================================================
# GF-INITIATED OPEN RELATIONSHIP — she suggests it after a concrete trigger
# Trigger reasons: "flirt" (saw player flirting), "threesome" (participated),
#                  "caught" (caught player in the act)
# ============================================================

label _gf_suggests_open_rel(girl):

    python:
        _gs_trigger = getattr(girl, "_gf_open_rel_trigger", None) or {}
        _gs_other_gid = _gs_trigger.get("other_gid")
        _gs_reason = _gs_trigger.get("reason", "caught")
        _gs_other = GIRL_BY_ID.get(_gs_other_gid) if _gs_other_gid else None
        _gs_other_name = _gs_other.Name if _gs_other else _tl(_("someone"))
        print("[HAREM_GF_SUGGEST] %s suggests open relationship (Love=%d Inbt=%d trigger=%s other=%s)" % (girl.gid, girl.Love, girl.Inbt, _gs_reason, _gs_other_gid))

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. A message from [girl.Name]."

    # GF sends opening message — contextual based on trigger reason
    python:
        _gs_openers_by_reason = {
            "flirt": {
                "polyamorous": [
                    _tl(_("I saw you flirting with %s the other day. And you know what? I wasn't even mad. I think we should talk about opening things up.")) % _gs_other_name,
                    _tl(_("So... I noticed you and %s getting cozy. I've been thinking about it, and honestly, I don't mind. Maybe we don't have to be exclusive.")) % _gs_other_name,
                ],
                "monogamous": [
                    _tl(_("I saw you with %s. Flirting. It hurt, but... I've been thinking. I'd rather share you than pretend I didn't see it.")) % _gs_other_name,
                    _tl(_("Look, I saw what happened with %s. I'm not going to lie, it stung. But losing you would be worse. So... maybe we can figure something out.")) % _gs_other_name,
                ],
                "cute_sex": [
                    _tl(_("Um... I saw you with %s. You seemed happy. I cried a little, but then I thought... maybe I'd be okay with it? If I still matter to you.")) % _gs_other_name,
                    _tl(_("Promise you won't be mad? I saw you flirting with %s. And instead of being angry, I just thought... maybe this is okay. If you still want me too.")) % _gs_other_name,
                ],
                "hardcore_sex": [
                    _tl(_("Caught you flirting with %s. Don't bother denying it. Here's the thing, I don't care. But if you're going to do it, let's make it official.")) % _gs_other_name,
                    _tl(_("So, %s, huh? I saw you two. I'm not the jealous type, so let's just be honest about this. Open relationship. You in?")) % _gs_other_name,
                ],
                "_default": [
                    _tl(_("I noticed you and %s the other day. I've been thinking about it a lot. Maybe we could... not be exclusive? If you want.")) % _gs_other_name,
                    _tl(_("I saw you flirting with %s. I thought I'd be furious, but I wasn't. I think I'd be okay sharing you. What do you think?")) % _gs_other_name,
                ],
            },
            "threesome": {
                "polyamorous": [
                    _tl(_("After what happened with us and %s... I can't stop thinking about it. I think we should do this for real. Open things up.")) % _gs_other_name,
                    _tl(_("That thing with %s was amazing. And it made me realize, I'm okay with sharing. More than okay, actually. Let's make it official.")) % _gs_other_name,
                ],
                "monogamous": [
                    _tl(_("I keep thinking about what we did with %s. I never thought I'd say this, but... maybe we don't need to be just us. If you want.")) % _gs_other_name,
                    _tl(_("After %s... I can't pretend I didn't enjoy it. And if that's something you want more of, I think I could handle it. Just be honest with me.")) % _gs_other_name,
                ],
                "cute_sex": [
                    _tl(_("So um... ever since that time with %s, I've been feeling things. Confusing things. Maybe we could... try being open? If you want?")) % _gs_other_name,
                    _tl(_("I haven't stopped thinking about %s. About all of us together. Is it weird that I want more of that? Can we talk about this?")) % _gs_other_name,
                ],
                "hardcore_sex": [
                    _tl(_("That threesome with %s was hot. Let's stop pretending we're vanilla. Open relationship. I'm in if you are.")) % _gs_other_name,
                    _tl(_("After %s, we both know this isn't a normal relationship anymore. Let's just own it. You can see other girls, I don't care.")) % _gs_other_name,
                ],
                "_default": [
                    _tl(_("What happened with %s changed something for me. I've been thinking... maybe we could see other people. Together or apart.")) % _gs_other_name,
                    _tl(_("I can't get %s out of my head. And I think... maybe that's okay. Maybe we should talk about opening things up.")) % _gs_other_name,
                ],
            },
            "caught": {
                "polyamorous": [
                    _tl(_("I caught you with %s. And honestly? I wasn't surprised. I've known for a while that I'm okay sharing you. Let's just make it official.")) % _gs_other_name,
                    _tl(_("So, %s. I saw everything. But here's the thing, I don't want to fight about it. I want to open things up. For real.")) % _gs_other_name,
                ],
                "monogamous": [
                    _tl(_("I caught you with %s. It broke my heart. But... I'd rather have you like this than not at all. Can we try an open thing?")) % _gs_other_name,
                    _tl(_("I know about %s. I saw you two. I've been crying about it, but... the thought of leaving you is worse. So let's just... make rules for it.")) % _gs_other_name,
                ],
                "cute_sex": [
                    _tl(_("I... I caught you with %s. I didn't know what to do. But then I thought, maybe... maybe I could share you? Please don't hate me for saying that.")) % _gs_other_name,
                    _tl(_("You were with %s. I saw. I was so scared and confused, but... I don't want to lose you. So if this is what you need, I'll try.")) % _gs_other_name,
                ],
                # dictating the terms is femdom, not hardcore (docs/plan_femdom.md D3)
                "femdom": [
                    _tl(_("So, %s. You got caught. Here's the deal: I don't care, but I'm not being the idiot who doesn't know. Open relationship. Take it or leave it.")) % _gs_other_name,
                    _tl(_("I saw you with %s. Here's what happens now: we open this up, and I make the rules. First rule, you tell me everything.")) % _gs_other_name,
                    _tl(_("You and %s. Caught. I'm not yelling, I'm deciding. From now on it's an open relationship, on my terms.")) % _gs_other_name,
                ],
                "hardcore_sex": [
                    _tl(_("Caught you with %s. Don't look so scared, I'm not here to yell. I'm here to tell you I'm fine with it. Let's just be open about it.")) % _gs_other_name,
                    _tl(_("Saw you with %s. Honestly? My heart was pounding, and not from anger. Open relationship? I can handle it.")) % _gs_other_name,
                ],
                "_default": [
                    _tl(_("I caught you with %s. I've been thinking about it a lot. And... I think I'd rather share you openly than wonder behind your back.")) % _gs_other_name,
                    _tl(_("I know about you and %s. Instead of being angry, I want to talk. Maybe we could... not be exclusive. If you're honest about it.")) % _gs_other_name,
                ],
            },
        }
        _gs_reason_pool = _gs_openers_by_reason.get(_gs_reason, _gs_openers_by_reason["caught"])
        _gs_line = None
        # femdom before hardcore_sex (docs/plan_femdom.md D3); a reason without a pool for her trait falls to the next one
        for _t in ("polyamorous", "monogamous", "cute_sex", "femdom", "hardcore_sex"):
            if girl.has_trait(_t) and _t in _gs_reason_pool:
                _gs_line = renpy.random.choice(_gs_reason_pool[_t])
                print("[HAREM_GF_SUGGEST] opener pool: %s / %s" % (_gs_reason, _t))
                break
        if _gs_line is None:
            _gs_line = renpy.random.choice(_gs_reason_pool["_default"])

    $ phone_add_msg(girl.gid, girl.gid, _gs_line)
    call screen phone_chat_screen(girl, auto_close=0, choices=[(_("Accept"), "accept"), (_("Decline"), "decline")])
    $ _gs_choice = _return

    if _gs_choice == "accept":
        $ phone_add_msg(girl.gid, "player", _tl(_("I'd like that. Thank you for trusting me with this.")))
        call screen phone_chat_screen(girl, auto_close=0.6, choices=[])

        # Girl responds relieved
        python:
            _gs_relief = {
                "polyamorous": [
                    _("I'm glad you feel the same way. This is going to be good for us."),
                ],
                "monogamous": [
                    _("Okay. Just... don't forget about me, alright?"),
                ],
                "cute_sex": [
                    _("Really? Oh god, I was so nervous. Okay. Okay, let's do this."),
                ],
                "hardcore_sex": [
                    _("Good. Just remember who brought it up first."),
                ],
                "_default": [
                    _("I'm happy you said yes. Let's see where this goes."),
                ],
            }
            _gs_rline = None
            for _t in ("polyamorous", "monogamous", "cute_sex", "hardcore_sex"):
                if girl.has_trait(_t):
                    _gs_rline = renpy.random.choice(_gs_relief[_t])
                    break
            if _gs_rline is None:
                _gs_rline = renpy.random.choice(_gs_relief["_default"])

        call _phone_typing(girl) from _call_gf_suggest_typing_1
        $ phone_add_msg(girl.gid, girl.gid, _gs_rline)
        call screen phone_chat_screen(girl, auto_close=0, choices=[])

        # Finalize: set consent, create/join harem group, bilateral harem
        python:
            girl._open_relationship_consent = True
            _hg = _get_harem_group()
            if _hg is None:
                _create_harem_group(girl)
                _hg = _get_harem_group()
                phone_group_add_msg(_hg["id"], "system", _tl(_("%s opened the relationship.")) % girl.Name, "system")
            else:
                if girl.gid not in _hg["members"]:
                    _hg["members"].append(girl.gid)
                    phone_group_add_msg(_hg["id"], "system", _tl(_("%s joined the group.")) % girl.Name, "system")

            for _gid in list(_hg["members"]):
                if _gid != girl.gid:
                    _other = GIRL_BY_ID.get(_gid)
                    if _other:
                        add_to_harem(girl, _gid)
                        add_to_harem(_other, girl.gid)

            print("[HAREM_GF_SUGGEST] %s accepted by player. Group=%s" % (girl.gid, _hg["id"]))

    else:
        $ phone_add_msg(girl.gid, "player", _tl(_("I appreciate you saying that, but I'm happy with just us.")))
        call screen phone_chat_screen(girl, auto_close=0.6, choices=[])

        python:
            _gs_decline = {
                "polyamorous": [
                    _("Oh. Well, that's sweet actually. But the offer stands if you ever change your mind."),
                ],
                "cute_sex": [
                    _("Wait, really? You just want me? That's... actually the best thing you could have said."),
                ],
                "_default": [
                    _("That's okay. I just wanted you to know how I feel. We're good."),
                ],
            }
            _gs_dline = None
            for _t in ("polyamorous", "cute_sex"):
                if girl.has_trait(_t):
                    _gs_dline = renpy.random.choice(_gs_decline[_t])
                    break
            if _gs_dline is None:
                _gs_dline = renpy.random.choice(_gs_decline["_default"])

        call _phone_typing(girl) from _call_gf_suggest_typing_2
        $ phone_add_msg(girl.gid, girl.gid, _gs_dline)
        call screen phone_chat_screen(girl, auto_close=0, choices=[])

        python:
            Change_Status(girl, "Love", 10)
            girl._open_rel_declined_day = store.Day   # was store.day (never existed): the cooldown compared 0 with 0 forever
            print("[HAREM_GF_SUGGEST] %s declined by player, Love +10" % girl.gid)

    # Clear trigger regardless of outcome
    $ girl._gf_open_rel_trigger = None
    return


# ============================================================
# PROPOSE MEMBER — player proposes adding a girl to the harem group
# ============================================================

label _harem_propose_member(group):

    python:
        _pm_candidates = _harem_propose_candidates()
        print("[HAREM_PROPOSE] candidates: %s" % [c.gid for c in _pm_candidates])

    if not _pm_candidates:
        $ phone_group_add_msg(group["id"], "system", _("No one else to add right now."), "system")
        return

    # Build candidate choice list
    python:
        _pm_choices = [(c.Name, c.gid) for c in _pm_candidates]

    call screen phone_group_chat_screen(group, choices=_pm_choices)
    $ _pm_pick = _return

    if _pm_pick in ("close", "home", "_typing_done"):
        return

    python:
        _pm_target = GIRL_BY_ID.get(_pm_pick)
        _pm_target_name = _pm_target.Name if _pm_target else _pm_pick
        print("[HAREM_PROPOSE] Player proposes %s" % _pm_pick)

    if _pm_target is None:
        return

    # Player sends proposal message
    $ phone_group_add_msg(group["id"], "player", _tl(_("What if we add %s to our group?")) % _pm_target_name)
    call screen phone_group_chat_screen(group, auto_close=0.6)

    # A member who is away (giving birth) cannot vote, and the group does not decide without her
    # (_harem_away_members). The button stays; he asks again when everybody is back.
    python:
        _pm_away = _harem_away_members(group)
    if _pm_away:
        $ print("[HAREM_PROPOSE] no vote: %s away" % [g.gid for g in _pm_away])
        $ phone_group_add_msg(group["id"], "system", _tl(_("Away right now: %s. The group won't decide without everyone. Ask again later.")) % format_name_list([g.Name for g in _pm_away]), "system")
        call screen phone_group_chat_screen(group, auto_close=1.2)
        return

    # Sequential voting
    python:
        _pm_voters = [gid for gid in group["members"]]
        _pm_all_accept = True
        _pm_rejector_gid = None
        _pm_rejector_reason = None
        _pm_votes = []

        _HAREM_VOTE_ACCEPT = {
            "poly": [
                _("Sure! The more the merrier, right?"),
                _("I'm fine with it. Love is not a competition."),
                _("Absolutely! I think she'd be great with us."),
                _("Always room for one more~ I say yes!"),
            ],
            "willing": [
                _("I think %s could fit in with us. I'm okay with it."),
                _("She seems cool. Yeah, I wouldn't mind."),
                _("%s? Sure, I could see that working."),
                _("I think I'd be fine with %s around."),
                _("Hmm, %s... yeah, why not? I'm open to it."),
            ],
            "likes_her": [
                _("I actually like %s. I'd be happy to have her around."),
                _("%s? Yeah, I get along with her. I'm in."),
                _("Oh, %s! I like her. That would be nice actually."),
                _("I'd love that! %s and I already get along well."),
            ],
            "forced": [
                _("... Fine. Whatever you want."),
                _("I don't like this. But I'll deal with it."),
                _("She can stay. Don't expect me to be nice about it."),
                _("You're lucky I... okay. Fine. But she better not start anything."),
            ],
        }
        _HAREM_VOTE_REJECT = {
            "unwilling": [
                _("No. I'm already sharing more than I'm comfortable with."),
                _("I don't think I can handle another person in this. Sorry."),
                _("Adding someone else? That's too much for me right now."),
                _("I barely got used to this arrangement. No more, please."),
            ],
            "hostile": [
                _("Absolutely not. I can't stand %s. That's where I draw the line."),
                _("%s? Seriously? She and I don't get along. No way."),
                _("If %s joins, I'm out. And I mean it."),
                _("You want %s here? Hard no. Not happening."),
            ],
        }

    # Build vote list in Python, then replay sequentially
    python:
        _pm_vote_results = []
        _pm_all_accept = True
        _pm_rejector_gid = None
        _pm_rejector_reason = None

        for _pm_v_gid in _pm_voters:
            _pm_voter = GIRL_BY_ID.get(_pm_v_gid)
            if _pm_voter is None:
                continue

            _pm_vr, _pm_vs, _pm_vk = harem_vote_on_girl(_pm_voter, _pm_target)

            if _pm_vr == "accept":
                _pm_pool = _HAREM_VOTE_ACCEPT.get(_pm_vk, _HAREM_VOTE_ACCEPT["willing"])
                _pm_vote_line = renpy.random.choice(_pm_pool)
                if _pm_vk == "forced":
                    _pm_fb = getattr(_pm_voter, "_harem_forced_by", None)
                    if _pm_fb is None:
                        _pm_voter._harem_forced_by = set()
                        _pm_fb = _pm_voter._harem_forced_by
                    _pm_fb.add(_pm_target.gid)
                    print("[HAREM] %s forced to accept %s via group vote" % (_pm_voter.gid, _pm_target.gid))
            else:
                _pm_pool = _HAREM_VOTE_REJECT.get(_pm_vk, _HAREM_VOTE_REJECT["unwilling"])
                _pm_vote_line = renpy.random.choice(_pm_pool)
                _pm_all_accept = False
                _pm_rejector_gid = _pm_v_gid
                _pm_rejector_reason = _pm_vk

            if "%s" in _pm_vote_line:
                _pm_vote_line = _pm_vote_line % _pm_target_name

            _pm_vote_results.append((_pm_v_gid, _pm_vr, _pm_vote_line))
            if not _pm_all_accept:
                break

    # Replay votes with typing animation
    $ _pm_vi = 0
    while _pm_vi < len(_pm_vote_results):
        python:
            _pm_vr_gid, _pm_vr_res, _pm_vr_line = _pm_vote_results[_pm_vi]

        $ phone_group_add_msg(group["id"], _pm_vr_gid, None, "typing")
        $ _pm_type_delay = renpy.random.uniform(1.0, 2.0)
        call screen phone_group_chat_screen(group, auto_close=_pm_type_delay)
        python:
            _g_msgs = phone_group_get_msgs(group["id"])
            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                _g_msgs.pop()
            phone_group_add_msg(group["id"], _pm_vr_gid, _pm_vr_line, "text")
        call screen phone_group_chat_screen(group, auto_close=0.5)

        $ _pm_vi += 1

    if _pm_all_accept:
        python:
            phone_group_add_msg(group["id"], "system", _tl(_("The girls seem open to %s joining. Ask her out to make it official!")) % _pm_target_name, "system")
            print("[HAREM_PROPOSE] All members open to %s (consultation only)" % _pm_target.gid)

        call screen phone_group_chat_screen(group, auto_close=1.0)
    else:
        python:
            _rej_name = _girl_name_by_gid(_pm_rejector_gid) if _pm_rejector_gid else _("Someone")
            phone_group_add_msg(group["id"], "system", _tl(_("%s isn't on board with adding %s.")) % (_rej_name, _pm_target_name), "system")
            print("[HAREM_PROPOSE] %s rejected by %s (%s)" % (_pm_target.gid, _pm_rejector_gid, _pm_rejector_reason))

        call screen phone_group_chat_screen(group, auto_close=1.0)

    return


# ============================================================
# HAREM GROUP EVENTS — trait-based phone chat sequences
# ============================================================

init python:

    _HAREM_TRAIT_PRIORITY = [
        "cum_slut", "camera_lover", "exhibitionist", "bisexual",
        "polyamorous", "monogamous", "hardcore_sex", "cute_sex",
    ]

    def _pick_harem_trait_line(girl, pools, name=None):
        # an eager trait she is still discovering speaks only through its discovery key (trait_line_keys)
        line = None
        for t in _HAREM_TRAIT_PRIORITY:
            if not girl.has_trait(t):
                continue
            _k = next((_tk for _tk in trait_line_keys(girl, t) if _tk in pools), None)
            if _k:
                line = renpy.random.choice(pools[_k])
                break
        if line is None:
            line = renpy.random.choice(pools["_default"])
        if name and "%s" in line:
            line = line % name
        return line

    # -- Group creation (2nd GF): existing GF response --
    _HAREM_INTRO_EXISTING = {
        "cum_slut": [
            _("A group to plan our sessions? Count me in!"),
            _("This makes planning our fun way easier~"),
        ],
        "camera_lover": [
            _("Nice! Now we can share pics here too~"),
            _("A group chat! Perfect for sharing our... content hehe"),
        ],
        "exhibitionist": [
            _("A group? Now we can plan some real shows~"),
            _("Love it! The more people involved, the more exciting it gets."),
        ],
        "bisexual": [
            _("Ooh, another girl in the mix? Honestly... I wouldn't mind getting closer to her myself~"),
            _("Her too, huh? I've caught myself curious about her. This could be fun for all of us."),
        ],
        "polyamorous": [
            _("Love it! The more connected we are, the better~"),
            _("A group for us? Finally! This is going to be amazing."),
        ],
        "monogamous": [
            _("I... guess this is really happening. Okay."),
            _("A group chat. Right. This is my life now."),
        ],
        "hardcore_sex": [
            _("A group chat for this? Fine, but I better get my share of attention."),
            _("Good. Now I can keep tabs on both of you."),
        ],
        "cute_sex": [
            _("A group for us! That's so sweet!"),
            _("Aww, this feels official now! I love it!"),
        ],
        "_default": [
            _("That makes things easier, good idea!"),
            _("Not bad. At least we'll all be on the same page."),
            _("Sure, why not? Let's see how this goes."),
        ],
    }

    # -- Group creation (2nd GF): new GF response --
    _HAREM_INTRO_NEW = {
        "cum_slut": [
            _("I liked the 'together' part hehe. What do you have in mind?"),
            _("Ooh, group plans? I'm already imagining things~"),
        ],
        "camera_lover": [
            _("A group? This is going to make for some great stories~"),
            _("I'm already thinking about what we could record together hehe"),
        ],
        "exhibitionist": [
            _("Together? Now you're speaking my language~"),
            _("Sounds fun! I love being the center of attention hehe"),
        ],
        "polyamorous": [
            _("This is going to be so much fun! Can't wait~"),
            _("I love this already! Group activities when?"),
        ],
        "monogamous": [
            _("I'm still getting used to all this. But hi everyone!"),
            _("This is a lot to process. But... hi."),
        ],
        "hardcore_sex": [
            _("I liked the 'something fun together' part. When do we start?"),
            _("A group for planning our sessions? I'm very interested."),
        ],
        "cute_sex": [
            _("This is exciting! And a little scary hehe"),
            _("I'm nervous but... I liked the second part hehe"),
        ],
        "_default": [
            _("I liked the second part hehe"),
            _("Hey! Glad to be here. This should be interesting~"),
            _("A group already? You move fast hehe. I like it."),
        ],
    }

    # -- Welcome (3rd+ GF): existing member greets new girl --
    _HAREM_WELCOME_EXISTING = {
        "cum_slut": [
            _("Welcome girl! I'll share with you, but his cum is still mine alone hahaha"),
            _("Yay, new girl! Just remember, I get first dibs on the good stuff~"),
        ],
        "camera_lover": [
            _("Nice, one more for our private recordings!"),
            _("Ooh, fresh face for the camera! Welcome %s!"),
        ],
        "exhibitionist": [
            _("The bigger the audience, the better~ Welcome!"),
            _("More people means more fun to show off to! Welcome!"),
        ],
        "polyamorous": [
            _("The more the merrier! Welcome, gorgeous~"),
            _("I love it! Welcome to the family, %s!"),
        ],
        "monogamous": [
            _("Wow, that's a lot of people now... but welcome!"),
            _("Another one? Well... welcome, I guess."),
        ],
        "hardcore_sex": [
            _("Fresh meat! Welcome to the fun side."),
            _("About time we got some new energy in here. Welcome %s!"),
        ],
        "cute_sex": [
            _("Hiiii %s! Welcome! This is going to be so fun!"),
            _("Omg yay! Welcome to the group!"),
        ],
        "_default": [
            _("Welcome to the group, %s!"),
            _("Hey %s! Glad to have you here!"),
            _("Look at us growing hehe. Welcome!"),
            _("Welcome! Things are about to get a lot more interesting~"),
        ],
    }

    # -- Welcome (3rd+ GF): new girl's response --
    _HAREM_WELCOME_NEW = {
        "cum_slut": [
            _("Hi girls! I hope you're all ready to share hehe~"),
            _("Hey! Something tells me we're all going to get along great~"),
        ],
        "camera_lover": [
            _("Hi! I have a feeling this group is going to have some amazing content~"),
            _("Hey everyone! Can't wait to see what we get up to~"),
        ],
        "exhibitionist": [
            _("Hi everyone! I promise to put on a good show~"),
            _("Hey! The more eyes, the better. Happy to be here!"),
        ],
        "polyamorous": [
            _("Finally! I've been waiting for this~ Hey girls!"),
            _("Yesss! Hi everyone! So happy to be here!"),
        ],
        "monogamous": [
            _("This is... a lot. But thanks for having me."),
            _("Hi everyone. I'm still processing this hehe."),
        ],
        "hardcore_sex": [
            _("So when's the party starting?"),
            _("Finally! I've been wanting to join the fun."),
        ],
        "cute_sex": [
            _("Omg hi everyone! I'm so excited and nervous hehe"),
            _("Hi! I can't believe this is happening!"),
        ],
        "_default": [
            _("Hey everyone! Happy to be here~"),
            _("Hi! Thanks for having me, this is going to be fun!"),
            _("Hello! I promise I'll be a good addition hehe"),
        ],
    }

    # -- Rivalry pools (forced acceptance) --
    _HAREM_INTRO_RIVAL_EXISTING = [
        _("Oh, %s is here? Great. Let's see how long this lasts."),
        _("Hi, %s. Just so you know, I'm the one he comes to first."),
        _("Welcome, %s. Don't get too comfortable."),
        _("So %s is joining. Fine. But I know who his favorite is."),
    ]
    _HAREM_INTRO_RIVAL_NEW = [
        _("Hey, %s! Let's see who makes him happier, shall we?"),
        _("Hi %s. I'll try to get along. No promises though haha"),
        _("Don't worry about me, %s. I plan to earn my place here."),
        _("Hi %s! I bet things are about to get way more interesting."),
    ]
    _HAREM_WELCOME_RIVAL_EXISTING = [
        _("Oh, %s. Welcome, I guess. Let's see what you've got."),
        _("Hey %s. Hope you can keep up."),
        _("%s? This should be interesting. Try not to bore him."),
        _("Welcome %s. I'm still his favorite though."),
    ]
    _HAREM_WELCOME_RIVAL_NEW = [
        _("Thanks for the warm welcome. I'll make sure to earn my spot."),
        _("Hi everyone! Don't worry, I'll prove I belong here."),
        _("Hey! I can already tell this is going to be a fun competition."),
        _("Hi girls! I'm sure we'll figure out who's the best hehe"),
    ]


# ── Group Intro Event (2nd GF joins) ─────────────────────────────
label _harem_group_intro_event(group, first_gf, new_girl):

    python:
        _hgi_player_msg = _tl(_("Hey %s. I need to be honest with you. I've grown close to %s too, and I don't want to hide it or make anyone a secret. I'd like the three of us to be together, openly, as one relationship. That's why I made this group. Would you be okay with that?")) % (first_gf.Name, new_girl.Name)
        phone_group_add_msg(group["id"], "player", _hgi_player_msg)
    call screen phone_group_chat_screen(group, auto_close=0.8)

    # Existing GF responds (rival pool if forced)
    python:
        _hgi_is_rival = new_girl.gid in getattr(first_gf, "_harem_forced_by", set())
        if _hgi_is_rival:
            _hgi_gf1_line = renpy.random.choice(_HAREM_INTRO_RIVAL_EXISTING)
            if "%s" in _hgi_gf1_line:
                _hgi_gf1_line = _hgi_gf1_line % new_girl.Name
        else:
            _hgi_gf1_line = _pick_harem_trait_line(first_gf, _HAREM_INTRO_EXISTING)
    $ phone_group_add_msg(group["id"], first_gf.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.2, 2.0))
    python:
        _hgi_msgs = phone_group_get_msgs(group["id"])
        if _hgi_msgs and _hgi_msgs[-1].get("type") == "typing":
            _hgi_msgs.pop()
        phone_group_add_msg(group["id"], first_gf.gid, _hgi_gf1_line)
    call screen phone_group_chat_screen(group, auto_close=0.6)

    # New GF responds (rival pool if forced)
    python:
        _hgi_new_is_rival = first_gf.gid in getattr(new_girl, "_harem_forced_by", set()) or _hgi_is_rival
        if _hgi_new_is_rival:
            _hgi_gf2_line = renpy.random.choice(_HAREM_INTRO_RIVAL_NEW)
            if "%s" in _hgi_gf2_line:
                _hgi_gf2_line = _hgi_gf2_line % first_gf.Name
        else:
            _hgi_gf2_line = _pick_harem_trait_line(new_girl, _HAREM_INTRO_NEW)
    $ phone_group_add_msg(group["id"], new_girl.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
    python:
        _hgi_msgs = phone_group_get_msgs(group["id"])
        if _hgi_msgs and _hgi_msgs[-1].get("type") == "typing":
            _hgi_msgs.pop()
        phone_group_add_msg(group["id"], new_girl.gid, _hgi_gf2_line)
    call screen phone_group_chat_screen(group)

    return


# ── Welcome New Member Event (3rd+ GF joins) ─────────────────────
label _harem_welcome_new_member(group, new_girl):

    python:
        _hwm_player_msg = _tl(_("Girls, I want to make this official: %s is joining our relationship. She means a lot to me, and I hope you'll welcome her as one of us.")) % new_girl.Name
        phone_group_add_msg(group["id"], "player", _hwm_player_msg)
    call screen phone_group_chat_screen(group, auto_close=0.8)

    # Each existing member welcomes with typing animation (rival pool if forced)
    python:
        _hwm_members = [gid for gid in group["members"] if gid != new_girl.gid]
        _hwm_responses = []
        _hwm_any_rival = False
        for _hwm_gid in _hwm_members:
            _hwm_g = GIRL_BY_ID.get(_hwm_gid)
            if _hwm_g and not girl_is_away(_hwm_g):   # away (giving birth): she is not reading the group
                _hwm_is_rival = new_girl.gid in getattr(_hwm_g, "_harem_forced_by", set())
                if _hwm_is_rival:
                    _hwm_any_rival = True
                    _hwm_line = renpy.random.choice(_HAREM_WELCOME_RIVAL_EXISTING)
                    if "%s" in _hwm_line:
                        _hwm_line = _hwm_line % new_girl.Name
                else:
                    _hwm_line = _pick_harem_trait_line(_hwm_g, _HAREM_WELCOME_EXISTING, new_girl.Name)
                _hwm_responses.append((_hwm_gid, _hwm_line))

    $ _hwm_i = 0
    while _hwm_i < len(_hwm_responses):
        python:
            _hwm_r_gid, _hwm_r_line = _hwm_responses[_hwm_i]
        $ phone_group_add_msg(group["id"], _hwm_r_gid, None, "typing")
        call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 2.0))
        python:
            _hwm_msgs = phone_group_get_msgs(group["id"])
            if _hwm_msgs and _hwm_msgs[-1].get("type") == "typing":
                _hwm_msgs.pop()
            phone_group_add_msg(group["id"], _hwm_r_gid, _hwm_r_line)
        call screen phone_group_chat_screen(group, auto_close=0.5)
        $ _hwm_i += 1

    # New girl responds (rival pool if any member is a rival)
    python:
        if _hwm_any_rival:
            _hwm_new_line = renpy.random.choice(_HAREM_WELCOME_RIVAL_NEW)
        else:
            _hwm_new_line = _pick_harem_trait_line(new_girl, _HAREM_WELCOME_NEW)
    $ phone_group_add_msg(group["id"], new_girl.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
    python:
        _hwm_msgs = phone_group_get_msgs(group["id"])
        if _hwm_msgs and _hwm_msgs[-1].get("type") == "typing":
            _hwm_msgs.pop()
        phone_group_add_msg(group["id"], new_girl.gid, _hwm_new_line)
    call screen phone_group_chat_screen(group)

    return
