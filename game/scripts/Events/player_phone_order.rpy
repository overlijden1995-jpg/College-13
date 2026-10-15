# ============================================================
# player_phone_order.rpy... HE texts a submissive girl an ORDER: be in his room tonight
# (docs/plan_submissive_pass.md S6, the mirror of Events/femdom_phone_order.rpy)
#
# SENT by him from her 1:1 chat (phone_messaging.rpy, the "Order" tile: submissive girls only, one pending order at a
# time for every girl together, PLAYER_PHONE_ORDER_COOLDOWN days between two orders to the same girl). The order is
# always for the NIGHT of that day. SHE ANSWERS on the spot through the approval engine (lewd "phone_order":
# ORDER_CONTROL "him", so her Control trait moves the Bonus): she obeys (deferent yes, Obed up) or apologizes.
# THAT NIGHT she is in HIS room (player_phone_order_tonight, read by update_all_girls_locations_for_time like the sleep
# arrangement), unless something closed her door (angry / sad / away / a partner catch pending): then the order is void.
# HE WALKS IN (player_phone_order_arrival, called by location_menu): her line, Love + Obed, the order is consumed.
# HE NEVER CAME: the first Wait after that Night (player_phone_order_judge) plays her hurt text: she waited for
# nothing, Love down. A night spent together anyway counts as kept.
# Lines: PLAYER_PHONE_ORDER_LINES[moment][gid] (her own voice), "_default" for a girl without one; while she is still
# discovering the trait (trait_is_discovering) only the "<moment>_new" pools speak.
# ============================================================

default _player_phone_order = None      # {"gid", "day", "slot"} of the pending order, or None

init python:

    PLAYER_PHONE_ORDER_COOLDOWN = 3         # days between two orders to the same girl
    PLAYER_PHONE_ORDER_LOVE = 5             # he was there when she came
    PLAYER_PHONE_ORDER_OBED = 10            # she obeyed: came and waited for him
    PLAYER_PHONE_ORDER_ACCEPT_OBED = 3      # she said yes
    PLAYER_PHONE_ORDER_STOOD_UP_LOVE = -15  # she waited in his room and he never came
    # Nights already taken by another event (the same list the femdom order reads)
    _PLAYER_PHONE_ORDER_BUSY_NIGHTS = ("_restaurant_day", "_hangout_scheduled_day", "_ag_scheduled_day", "_bet_scheduled_day")

    PLAYER_PHONE_ORDER_LINES = {
        # His order (the text he sends)
        "order": {
            "_default": [
                _("Be in my room tonight."),
                _("My room. Tonight. Don't be late."),
                _("Tonight you're sleeping in my room. Be there."),
            ],
        },

        # She obeys
        "accept": {
            "_default": [
                _("Yes. I'll be there. ...Is there anything you want me to bring?"),
                _("Okay. Tonight. I'll be waiting for you. Tell me if you change your mind, please."),
                _("Understood. I'll be in your room tonight. Thank you for telling me what to do."),
            ],
        },
        "accept_new": {
            "_default": [
                _("...Okay. Yes. I'll be there. It's weird how easy it was to say that."),
                _("Yes. Tonight. I didn't even think about it, I just... said yes. Huh."),
                _("Okay. I'll come. I don't know why being told feels better than being asked. It does."),
            ],
        },

        # She can't (the approval said no): deferent, never a push back
        "refuse": {
            "_default": [
                _("I'm sorry... I can't tonight. Please don't be mad that I said no."),
                _("I... I'm not ready for that yet. I'm sorry. Ask me again soon? Please?"),
                _("I want to say yes. I can't tonight. I'm sorry, I'll make it up to you."),
            ],
        },
        "refuse_new": {
            "_default": [
                _("I almost said yes without thinking. I can't tonight. ...Sorry. I don't know why I'm apologizing."),
                _("Not tonight... sorry. I keep wanting to just do what you say. That's new."),
            ],
        },

        # He walked into his room and she is there
        "arrived": {
            "_default": [
                _("You're here. I came as soon as it got dark, like you said. ...What do you want me to do?"),
                _("I've been waiting. I didn't touch anything. Tell me what you want."),
                _("Here, like you told me. ...Did I do good?"),
            ],
        },
        "arrived_new": {
            "_default": [
                _("I'm here. I kept checking the door. I don't know why waiting for you felt so right."),
                _("You told me to be here, so I'm here. ...I liked being told. That's strange, isn't it?"),
            ],
        },

        # The Night is over and he never came
        "no_show": {
            "_default": [
                _("I waited in your room until it got cold. Did I do something wrong?"),
                _("You told me to be there and you never came. I'm not angry. I just... need to know what I did."),
                _("I sat on your bed all night. If you didn't want me there, you could have said so. I would have understood."),
            ],
        },
        "no_show_new": {
            "_default": [
                _("I waited all night. It hurt more than it should. I'm still not angry at you. I don't know what that says about me."),
                _("You never came. I kept waiting anyway. ...Just tell me next time, please."),
            ],
        },
    }

    def player_phone_order_line(girl, moment):
        """Her line (English: the caller translates) for a moment of his order: her own voice first, the shared
        "_default" after. While she is still discovering the trait only the "<moment>_new" pools speak."""
        _key = moment + "_new" if (moment + "_new") in PLAYER_PHONE_ORDER_LINES and trait_is_discovering(girl, "submissive") else moment
        _table = PLAYER_PHONE_ORDER_LINES[_key]
        return renpy.random.choice(_table.get(girl.gid) or _table["_default"])

    def _player_phone_order_blocked(girl):
        """Why he can't order this girl to his room tonight (the tile's note / the log), or None when he can."""
        if not (hasattr(girl, "has_trait") and girl.has_trait("submissive")):
            return "not submissive"
        if store._player_phone_order is not None:
            return _("an order is pending")
        if store.TimeIndex >= NIGHT_INDEX:
            return _("too late")
        if girl.gid not in getattr(store.Player, "phone_contacts", set()):
            return _("no number")
        if getattr(girl, "loc", None) == store.CurrentLocation:
            return _("she is right here")
        if girl_is_away(girl) or girl.has_temp_status("angry") or girl.has_temp_status("sad") or girl.has_temp_status("unavailable"):
            return _("not now")
        if girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
            return _("not now")
        if getattr(girl, "_sleeps_in_player_room", False):
            return _("she sleeps here already")
        if girl.has_trait("married"):
            return _("she sleeps at home")
        for _flag in ("_npc_catch_pending", "_npc_catch_msg_pending", "_ntr_violation_pending",
                      "_npc_pregnancy_confrontation_pending"):
            if getattr(girl, _flag, False):
                return _("not now")
        if [_v for _v in _PLAYER_PHONE_ORDER_BUSY_NIGHTS if getattr(store, _v, -1) == store.Day]:
            return _("tonight is taken")
        _last = getattr(girl, "_player_order_day", 0) or 0
        if _last > 0 and store.Day - _last < PLAYER_PHONE_ORDER_COOLDOWN:
            return _("too soon")
        return None

    def player_phone_order_tile(girl, free):
        """The "Order" tile of her 1:1 chat (phone_chat_actions): submissive girls only, with the reason when it
        cannot be sent now. None = not a submissive (no tile)."""
        _why = _player_phone_order_blocked(girl)
        if _why == "not submissive":
            return None
        return _chat_tile((None if _why else "order"), _tl(_("Order")), "home", "#a855f7", free, (_tl(_why) if _why else None))

    def player_phone_order_check(girl):
        """Does she obey his order? The approval engine: lewd "phone_order" (Love AND Obed; ORDER_CONTROL "him", so
        her Control trait moves the Bonus). Remote: she answers on her phone."""
        _cfg = ApprovalRuleFor(girl=girl, action="phone_order", category="lewd")
        _dec = ApprovalCheck(girl=girl, T=_cfg["T"], Type=_cfg["Type"], Spread=_cfg["Spread"], Bonus=_cfg["Bonus"],
                             Variation=_cfg["Variation"], ReturnData=True, Action="phone_order",
                             Location=girl_home_loc(girl), Remote=True)
        print("[PLAYER_ORDER] %s: approval score=%s T=%s type=%s accepted=%s" % (
            girl.gid, _dec.get("score"), _cfg["T"], _cfg["Type"], _dec.get("accepted")))
        return bool(_dec.get("accepted"))

    def _player_phone_order_void_reason(girl):
        """Why her pending order no longer means anything (for the log), or None."""
        if girl is None:
            return "girl not found"
        if not girl.has_trait("submissive"):
            return "no longer submissive"
        if girl_is_away(girl):
            return "away"
        if girl.has_temp_status("angry") or girl.has_temp_status("sad"):
            return "angry / sad"
        if getattr(girl, "_npc_catch_pending", False):
            return "npc catch pending"
        return None

    def player_phone_order_tonight(girl, day, time_index):
        """update_all_girls_locations_for_time: she is in HIS room this Night, as he ordered. True = put her there."""
        _o = store._player_phone_order
        if not _o or _o["gid"] != girl.gid or _o["day"] != day or time_index != _o["slot"]:
            return False
        if _player_phone_order_void_reason(girl):
            return False
        return True

    def player_phone_order_judge():
        """label Wait 5g: the Night of his order is over. Returns the girl who waited for nothing (the caller plays
        _player_phone_order_no_show), else None. Kept and void orders end here without a word."""
        _o = store._player_phone_order
        if not _o:
            return None
        if (store.Day, store.TimeIndex) <= (_o["day"], _o["slot"]):
            return None
        store._player_phone_order = None
        _girl = GIRL_BY_ID.get(_o["gid"])
        _void = _player_phone_order_void_reason(_girl)
        if _void:
            print("[PLAYER_ORDER] order to %s (Day %d) is void: %s" % (_o["gid"], _o["day"], _void))
            return None
        if store.Day - _o["day"] > 1:
            print("[PLAYER_ORDER] order to %s (Day %d) is stale on Day %d: dropped" % (_girl.gid, _o["day"], store.Day))
            return None
        _with = getattr(store, "_girls_were_with_player", None) or set()
        if getattr(_girl, "_slept_with_player_tonight", False) or (store.CurrentLocation == "room" and _girl.gid in _with):
            # the night together happened anyway (he was in his room with her when it ended)
            Change_Status(_girl, "Love", PLAYER_PHONE_ORDER_LOVE)
            print("[PLAYER_ORDER] order to %s kept (night spent together), Love +%d" % (_girl.gid, PLAYER_PHONE_ORDER_LOVE))
            return None
        print("[PLAYER_ORDER] order to %s broken: he never came to his room" % _girl.gid)
        return _girl

    def player_phone_order_rollover():
        """_per_day_cleanup: an order older than last night is stale (nothing judged it): drop it."""
        _o = store._player_phone_order
        if _o and _o["day"] < store.Day - 1:
            print("[PLAYER_ORDER] order to %s (Day %d) dropped at the rollover to Day %d" % (_o["gid"], _o["day"], store.Day))
            store._player_phone_order = None

    def player_phone_order_arrival():
        """location_menu (the menu of every place): he is in his room, with her there, in the Night he ordered.
        Returns the girl waiting for him (the caller plays _player_phone_order_arrived), else None."""
        _o = store._player_phone_order
        if not _o or _o["day"] != store.Day or store.TimeIndex != _o["slot"]:
            return None
        _girl = GIRL_BY_ID.get(_o["gid"])
        if _girl is None or store.CurrentLocation != "room" or _girl.loc != "room":
            return None
        if _player_phone_order_void_reason(_girl):
            return None
        store._player_phone_order = None
        if _girl in store.Party:
            # she walked in with him: the night together is what he wanted, no "you came" line
            Change_Status(_girl, "Love", PLAYER_PHONE_ORDER_LOVE)
            print("[PLAYER_ORDER] order to %s kept (came to his room together), Love +%d" % (_girl.gid, PLAYER_PHONE_ORDER_LOVE))
            return None
        print("[PLAYER_ORDER] order to %s kept: he walked in on her waiting (Day %d)" % (_girl.gid, store.Day))
        return _girl

# ============================================================
# He sends the order from her chat (phone_messaging.rpy, the "Order" tile)
# ============================================================
label _player_phone_order_event(girl):
    $ phone_add_msg(girl.gid, "player", _tl(player_phone_order_line(girl, "order")))
    $ girl._player_order_day = Day
    call _phone_typing(girl, choices=[]) from _player_phone_order_typing
    if player_phone_order_check(girl):
        python:
            store._player_phone_order = {"gid": girl.gid, "day": Day, "slot": NIGHT_INDEX}
            phone_add_msg(girl.gid, girl.gid, _tl(player_phone_order_line(girl, "accept")))
            phone_add_msg(girl.gid, "system", _tl(_("%s will be in your room tonight.")) % girl.Name)
            girl.discover("discovered_trait_submissive")
            Change_Status(girl, "Obed", PLAYER_PHONE_ORDER_ACCEPT_OBED)
            print("[PLAYER_ORDER] %s obeys: his room tonight (Day %d, %s, discovering=%s)" % (
                girl.gid, Day, TIME_NAMES[TimeIndex], trait_is_discovering(girl, "submissive")))
    else:
        python:
            phone_add_msg(girl.gid, girl.gid, _tl(player_phone_order_line(girl, "refuse")))
            print("[PLAYER_ORDER] %s apologizes: not tonight" % girl.gid)
    return

# ============================================================
# He walked into his room that Night (player_phone_order_arrival from location_menu, face to face)
# ============================================================
label _player_phone_order_arrived(girl):
    $ set_scene_expression(girl, "shy", pose="standing")
    $ Say_Line(girl, player_phone_order_line(girl, "arrived"))
    $ Change_Status(girl, "Love", PLAYER_PHONE_ORDER_LOVE)
    $ Change_Status(girl, "Obed", PLAYER_PHONE_ORDER_OBED)
    $ set_scene_expression(girl, "normal", pose="standing")
    return

# ============================================================
# That Night is over and he never came (label Wait 5g): her hurt text, or her line when she is right there
# ============================================================
label _player_phone_order_no_show(girl):
    $ _ppo_line = player_phone_order_line(girl, "no_show")
    if getattr(girl, "loc", None) == CurrentLocation:
        $ set_scene_expression(girl, "sad", pose="standing")
        $ Say_Line(girl, _ppo_line)
        $ set_scene_expression(girl, "normal", pose="standing")
    else:
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Your phone buzzes. Someone sent you a message."))
        call _phone_typing(girl, choices=[]) from _player_phone_order_typing_no_show
        $ phone_add_msg(girl.gid, girl.gid, _tl(_ppo_line))
        call screen phone_chat_screen(girl, choices=[])
    $ Change_Status(girl, "Love", PLAYER_PHONE_ORDER_STOOD_UP_LOVE)
    return
