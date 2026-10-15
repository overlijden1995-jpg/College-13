# ============================================================
# femdom_phone_order.rpy... a femdom girl texts him an ORDER: be at her room tonight
# (docs/plan_femdom.md section 7, "Celular"; mechanics of the trait in Actions/femdom.rpy)
#
# SENT by label Wait (system_time.rpy, step 6l) in the Morning, Midday or Evening: FEMDOM_PHONE_ORDER_CHANCE x her
# femdom_intensity per Wait, one order pending at a time (for every girl together), FEMDOM_PHONE_ORDER_COOLDOWN days
# between two orders of the same girl. The order is always for the NIGHT of that day: every girl with a room sleeps
# there (her schedule), so nothing has to move her; a girl whose schedule says otherwise tonight never orders.
# HE ANSWERS in the phone: "I'll be there." (the order stands, Love comes when he shows up) / "Can't tonight."
# (refused on the spot: femdom_request_refused + her angry reply) / Back or Home at the answers (no answer: the
# order stands, and she expects him anyway).
# SHOWING UP: femdom_phone_order_arrival (called by location_menu, the menu of every place) sees him in her room,
# with her there, in that Night: her pleased line face to face + FEMDOM_PHONE_ORDER_LOVE.
# NOT SHOWING UP: the first Wait after that Night (step 5g, femdom_phone_order_judge) plays her angry text (or her line,
# when she is right there) + femdom_request_refused(girl, "phone_order"). A night spent together anyway
# (_slept_with_player_tonight) counts as kept. Away / angry / sad / no longer femdom by then = the order is void.
# Lines: FEMDOM_PHONE_ORDER_LINES[moment][gid] (her own voice), "_default" for a girl without one; while she is still
# discovering the trait (trait_is_discovering) only the "<moment>_new" pools speak (D7: never an old habit).
# ============================================================

default _femdom_phone_order = None      # {"gid", "day", "slot", "answer"} of the pending order, or None

init python:

    FEMDOM_PHONE_ORDER_CHANCE = 0.08        # per Wait (Morning / Midday / Evening), x femdom_intensity
    FEMDOM_PHONE_ORDER_COOLDOWN = 5         # days between two orders of the same girl
    FEMDOM_PHONE_ORDER_LOVE_MIN = 500       # she only orders someone she is close to
    FEMDOM_PHONE_ORDER_LOVE = 5             # he showed up (obeying her = Love up, plan D2)
    # 1+ of these done with him: she orders a lover to her room, not a stranger
    FEMDOM_PHONE_ORDER_ACTS = frozenset(("hj", "tj", "bj", "fj", "sex", "anal", "rub", "oral"))
    # Nights already taken by another event: no order for them (restaurant date, hangout in his room, anniversary
    # gift in hers, NTR bet)
    _FEMDOM_PHONE_ORDER_BUSY_NIGHTS = ("_restaurant_day", "_hangout_scheduled_day", "_ag_scheduled_day", "_bet_scheduled_day")

    FEMDOM_PHONE_ORDER_LINES = {
        # Her order (the first text)
        "order": {
            "gwen": [
                _("My room. Tonight. Consider it a challenge you can't turn down."),
                _("Clear your night. You're coming to my room. And no, that wasn't a question."),
                _("Tonight, my room. Don't make me come looking for you. You won't like it."),
            ],
            "rogue": [
                _("Tonight, sugar. My room. Don't keep me waitin'."),
                _("You're comin' over tonight, darlin'. That ain't a question."),
                _("My room, tonight. Be late and you'll hear about it, sugar."),
            ],
            "ntw": [
                _("My room. Tonight. Don't be late."),
                _("Tonight. My room. I don't repeat myself."),
                _("Be at my door tonight. Saying no is not an option."),
            ],
            "tenny": [
                _("U-um... my room. Tonight. I've already decided what I'm doing to you."),
                _("Th-this isn't a request... be in my room tonight. I made a list. It's long."),
                _("Tonight. My room. P-please don't be late, I'm not in a patient mood at all."),
            ],
            "_default": [
                _("Be at my room tonight. Don't be late."),
                _("Tonight. My room. That's not a request."),
                _("Clear your night. You're coming to my room."),
            ],
        },
        "order_new": {
            "_default": [
                _("Come to my room tonight. That's... an order, I think. I kind of like saying that."),
                _("Be at my room tonight. Huh. Telling you what to do feels better than I expected."),
                _("My room, tonight. I'm not asking. ...Wow, I've never texted anyone like that."),
            ],
        },

        # He answered "I'll be there."
        "obeyed": {
            "gwen": [
                _("Good answer. Let's see if you actually show up."),
                _("Look at you, following instructions. I'm almost impressed."),
                _("Smart choice. Be on time and I might even be nice."),
            ],
            "rogue": [
                _("That's what I like to hear, sugar."),
                _("Good boy. I'll be waitin', darlin'."),
                _("Atta boy. Don't make me come lookin' for you."),
            ],
            "ntw": [
                _("Good."),
                _("Correct answer."),
                _("Obviously. Don't make me regret texting you."),
            ],
            "tenny": [
                _("O-okay. Good. Really good. I'll be ready."),
                _("Good boy. Um. I'm going to keep saying that tonight."),
                _("Okay! I mean... good. I'll be waiting. Wearing almost nothing."),
            ],
            "_default": [
                _("Good. Don't keep me waiting."),
                _("That's what I wanted to hear."),
                _("Good boy. See you tonight."),
            ],
        },
        "obeyed_new": {
            "_default": [
                _("Good. Wow. I really like it when you just say yes."),
                _("Okay. That was easy. I could get used to this."),
                _("Good boy. ...Did I just call you that? I think I liked it."),
            ],
        },

        # He answered "Can't tonight."
        "refused": {
            "gwen": [
                _("Wow. Bold. I'll remember that."),
                _("Can't? Cute. I didn't ask if you could."),
                _("You just turned me down. Enjoy your boring night."),
            ],
            "rogue": [
                _("Excuse me? I wasn't askin', sugar."),
                _("Well, ain't you brave. You'll pay for that one, darlin'."),
                _("Fine. But don't you come cryin' to me later."),
            ],
            "ntw": [
                _("Wrong answer."),
                _("You don't get to say no to me."),
                _("Noted. You'll regret it."),
            ],
            "tenny": [
                _("Oh. O-okay. I'm... actually really mad about that."),
                _("You can't? B-but I planned everything... fine. I'll remember this."),
                _("That's... not the answer I wanted. At all."),
            ],
            "_default": [
                _("Excuse me? That wasn't a question."),
                _("Wrong answer. You'll make this up to me."),
                _("You're turning me down? Remember this."),
            ],
        },
        "refused_new": {
            "_default": [
                _("No? Huh. I really, really didn't like reading that."),
                _("Okay... I didn't expect it to make me this mad. I guess I like being obeyed."),
                _("You said no. I'm learning something about myself, and you're not going to like it."),
            ],
        },

        # He walked into her room that Night (face to face)
        "arrived": {
            "gwen": [
                _("Right on time. See? Following orders isn't that hard."),
                _("You actually came. Good. Now close the door."),
                _("Look who showed up. I knew you would."),
            ],
            "rogue": [
                _("There you are, sugar. Right on time."),
                _("Good boy. Now get over here, darlin'."),
                _("Knew you'd come. Close that door behind you."),
            ],
            "ntw": [
                _("Good. You listened."),
                _("On time. Acceptable."),
                _("You came. Now shut the door and wait for instructions."),
            ],
            "tenny": [
                _("Y-you came! I mean... good. Close the door. We have a lot to do."),
                _("You're here. Good boy. I've been thinking about this all day."),
                _("Right on time... okay. Okay. I'm in charge now. Just so you know."),
            ],
            "_default": [
                _("You came. Good. That's what I like."),
                _("Right on time. Good boy."),
                _("See? You can follow orders."),
            ],
        },
        "arrived_new": {
            "_default": [
                _("You came. Because I told you to. ...I really like that."),
                _("You actually listened. Huh. That feels amazing."),
                _("Right on time. I think I could get used to giving you orders."),
            ],
        },

        # That Night is over and he never came (her text, or her line when she is right there)
        "no_show": {
            "gwen": [
                _("I waited. You didn't come. Wow."),
                _("So my order was optional? Cute. It won't be next time."),
                _("You stood me up. Bold move. Let's see how that works out for you."),
            ],
            "rogue": [
                _("I waited up for you, sugar. You never showed."),
                _("I told you to come over. You didn't. We're gonna talk about that."),
                _("Don't you ever leave me waitin' like that again, darlin'."),
            ],
            "ntw": [
                _("You didn't come."),
                _("I gave you an order. You ignored it."),
                _("Don't bother apologizing. Just remember it."),
            ],
            "tenny": [
                _("I waited. You didn't come. I'm so mad I can't even stutter properly."),
                _("I told you to come... and you didn't. I h-had plans for you."),
                _("You didn't show up. I'm... really, really angry. Just so you know."),
            ],
            "_default": [
                _("I told you to come. You didn't."),
                _("I waited. You never showed up."),
                _("You ignored my order. Don't do that again."),
            ],
        },
        "no_show_new": {
            "_default": [
                _("I told you to come and you didn't. I hate how much that bothers me."),
                _("You didn't show up. Huh. I didn't know being ignored could make me this angry."),
                _("I waited. I'm finding out I really don't like being disobeyed."),
            ],
        },
    }

    def femdom_phone_order_line(girl, moment):
        """Her line (English: the caller translates) for a moment of the phone order: her own voice first, the
        shared "_default" after. While she is still discovering the trait only the "<moment>_new" pools speak."""
        _key = moment + "_new" if trait_is_discovering(girl, "femdom") else moment
        _table = FEMDOM_PHONE_ORDER_LINES[_key]
        return renpy.random.choice(_table.get(girl.gid) or _table["_default"])

    def _femdom_phone_order_blocked(girl, with_player):
        """Why this femdom girl can't text him an order now (a reason for the log), or None when she can."""
        _room = GIRL_ROOMS.get(girl.gid)
        if not _room or _room not in _LOC_LOOPS:
            return "no room of her own"
        if get_scheduled_location_for(girl, store.Day, NIGHT_INDEX) != _room:
            return "not home tonight"
        if getattr(girl, "_sleeps_in_player_room", False):
            return "sleeps in his room"
        if girl.gid not in getattr(store.Player, "phone_contacts", set()):
            return "no phone contact"
        if getattr(girl, "loc", None) == store.CurrentLocation or girl.gid in with_player:
            return "with him"
        if girl.has_temp_status("angry") or girl.has_temp_status("sad") or girl.has_temp_status("unavailable"):
            return "angry / sad / unavailable"
        for _flag in ("_npc_catch_pending", "_npc_catch_msg_pending", "_ntr_violation_pending",
                      "_npc_pregnancy_confrontation_pending"):
            if getattr(girl, _flag, False):
                return _flag
        if girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
            return "ex before the confrontation"
        if girl.has_npc_partner():
            return "has a partner"
        _last = getattr(girl, "_femdom_order_day", 0) or 0
        if _last > 0 and store.Day - _last < FEMDOM_PHONE_ORDER_COOLDOWN:
            return "cooldown (last order Day %d)" % _last
        if girl.Love < FEMDOM_PHONE_ORDER_LOVE_MIN:
            return "Love %d" % girl.Love
        if not (getattr(girl, "intimacy_flags", None) or set()).intersection(FEMDOM_PHONE_ORDER_ACTS):
            return "nothing sexual with him yet"
        return None

    def femdom_phone_order_pick():
        """label Wait 6l: the femdom girl who texts him an order now, or None."""
        if store._femdom_phone_order is not None or store.TimeIndex >= NIGHT_INDEX:
            return None
        _busy = [_v for _v in _FEMDOM_PHONE_ORDER_BUSY_NIGHTS if getattr(store, _v, -1) == store.Day]
        if _busy:
            return None
        _with = getattr(store, "_girls_were_with_player", None) or set()
        _cands = [_g for _g in girls_reachable() if femdom_intensity(_g)]
        renpy.random.shuffle(_cands)
        for _g in _cands:
            _why = _femdom_phone_order_blocked(_g, _with)
            if _why:
                print("[FEMDOM] phone order: %s can't order him tonight (%s)" % (_g.gid, _why))
                continue
            _chance = FEMDOM_PHONE_ORDER_CHANCE * femdom_intensity(_g)
            if renpy.random.random() >= _chance:
                print("[FEMDOM] phone order: %s eligible, roll failed (chance %.2f)" % (_g.gid, _chance))
                continue
            return _g
        return None

    def _femdom_phone_order_void_reason(girl):
        """Why her pending order no longer means anything (for the log), or None."""
        if girl is None:
            return "girl not found"
        if not girl.has_trait("femdom"):
            return "no longer femdom"
        if girl_is_away(girl):
            return "away"
        if girl.has_temp_status("angry") or girl.has_temp_status("sad"):
            return "angry / sad (her door was closed to him anyway)"
        if getattr(girl, "_npc_catch_pending", False):
            return "npc catch pending (her room was blocked)"
        return None

    def femdom_phone_order_judge():
        """label Wait 5g: the Night of her order is over. Returns the girl who waited for nothing (the caller plays
        _femdom_phone_order_no_show), else None. Kept and void orders end here without a word."""
        _o = store._femdom_phone_order
        if not _o:
            return None
        if (store.Day, store.TimeIndex) <= (_o["day"], _o["slot"]):
            return None
        store._femdom_phone_order = None
        _girl = GIRL_BY_ID.get(_o["gid"])
        _void = _femdom_phone_order_void_reason(_girl)
        if _void:
            print("[FEMDOM] phone order of %s (Day %d) is void: %s" % (_o["gid"], _o["day"], _void))
            return None
        if store.Day - _o["day"] > 1:
            print("[FEMDOM] phone order of %s (Day %d) is stale on Day %d: dropped" % (_girl.gid, _o["day"], store.Day))
            return None
        _room = GIRL_ROOMS.get(_girl.gid)
        _with = getattr(store, "_girls_were_with_player", None) or set()
        if getattr(_girl, "_slept_with_player_tonight", False) or (store.CurrentLocation == _room and _girl.gid in _with):
            # the night together happened anyway (a sleepover, or he was with her in her room when it ended)
            Change_Status(_girl, "Love", FEMDOM_PHONE_ORDER_LOVE)
            print("[FEMDOM] phone order of %s kept (night spent together), Love +%d" % (_girl.gid, FEMDOM_PHONE_ORDER_LOVE))
            return None
        print("[FEMDOM] phone order of %s broken: he never came (answer=%s)" % (_girl.gid, _o.get("answer")))
        return _girl

    def femdom_phone_order_rollover():
        """_per_day_cleanup: an order older than last night is stale (nothing judged it): drop it."""
        _o = store._femdom_phone_order
        if _o and _o["day"] < store.Day - 1:
            print("[FEMDOM] phone order of %s (Day %d) dropped at the rollover to Day %d" % (_o["gid"], _o["day"], store.Day))
            store._femdom_phone_order = None

    def femdom_phone_order_arrival():
        """location_menu (the menu of every place): he is in her room, with her there, in the Night she ordered.
        Returns the girl who sees him walk in (the caller plays _femdom_phone_order_arrived), else None. A girl who
        walked in WITH him (Party) keeps the order without a line."""
        _o = store._femdom_phone_order
        if not _o or _o["day"] != store.Day or store.TimeIndex != _o["slot"]:
            return None
        _girl = GIRL_BY_ID.get(_o["gid"])
        _room = GIRL_ROOMS.get(_o["gid"])
        if _girl is None or store.CurrentLocation != _room or _girl.loc != _room:
            return None
        if girl_is_away(_girl) or _girl.has_temp_status("angry") or _girl.has_temp_status("sad"):
            return None
        store._femdom_phone_order = None
        if _girl in store.Party:
            # she walked in with him: the night together is what she wanted, no "you came" line
            Change_Status(_girl, "Love", FEMDOM_PHONE_ORDER_LOVE)
            print("[FEMDOM] phone order of %s kept (came to her room together), Love +%d" % (_girl.gid, FEMDOM_PHONE_ORDER_LOVE))
            return None
        print("[FEMDOM] phone order of %s kept: he is in her room (Day %d, answer=%s)" % (_girl.gid, store.Day, _o.get("answer")))
        return _girl

# ============================================================
# Her order arrives by text (label Wait 6l)
# ============================================================
label _femdom_phone_order_event(girl):
    python:
        store._femdom_phone_order = {"gid": girl.gid, "day": Day, "slot": NIGHT_INDEX, "answer": None}
        girl._femdom_order_day = Day
        print("[FEMDOM] phone order: %s orders him to her room tonight (Day %d, %s, discovering=%s)" % (
            girl.gid, Day, TIME_NAMES[TimeIndex], trait_is_discovering(girl, "femdom")))

    play sound "audio/Notification.mp3" noloop
    $ Narration(_("Your phone buzzes. Someone sent you a message."))

    call _phone_typing(girl, choices=[]) from _femdom_phone_order_typing_order
    $ phone_add_msg(girl.gid, girl.gid, _tl(femdom_phone_order_line(girl, "order")))
    $ girl.discover("discovered_trait_femdom")

    python:
        _fdo_choices = [
            (_tl(_("I'll be there.")), "obey"),
            (_tl(_("Can't tonight.")), "refuse"),
        ]
    call screen phone_chat_screen(girl, choices=_fdo_choices)
    $ _fdo_pick = _return

    if _fdo_pick == "obey":
        $ store._femdom_phone_order["answer"] = "yes"
        $ print("[FEMDOM] phone order: he answered he'll be at %s's room" % girl.gid)
        $ phone_add_msg(girl.gid, "player", _tl(_("I'll be there.")))
        call _phone_typing(girl, choices=[]) from _femdom_phone_order_typing_obey
        $ phone_add_msg(girl.gid, girl.gid, _tl(femdom_phone_order_line(girl, "obeyed")))
        call screen phone_chat_screen(girl, choices=[])

    elif _fdo_pick == "refuse":
        $ store._femdom_phone_order = None
        $ phone_add_msg(girl.gid, "player", _tl(_("Can't tonight.")))
        call _phone_typing(girl, choices=[]) from _femdom_phone_order_typing_refuse
        $ phone_add_msg(girl.gid, girl.gid, _tl(femdom_phone_order_line(girl, "refused")))
        $ femdom_request_refused(girl, "phone_order")
        call screen phone_chat_screen(girl, choices=[])

    else:
        # Back / Home at the answers: he put the phone away without a word. Her order stands.
        $ store._femdom_phone_order["answer"] = "none"
        $ print("[FEMDOM] phone order: he closed the phone without answering %s (%s): the order stands" % (girl.gid, _fdo_pick))

    return

# ============================================================
# He walked into her room that Night (femdom_phone_order_arrival from location_menu, face to face)
# ============================================================
label _femdom_phone_order_arrived(girl):
    $ set_scene_expression(girl, "smug", pose="standing")
    $ Say_Line(girl, femdom_phone_order_line(girl, "arrived"))
    $ Change_Status(girl, "Love", FEMDOM_PHONE_ORDER_LOVE)
    $ set_scene_expression(girl, "normal", pose="standing")
    return

# ============================================================
# That Night is over and he never came (label Wait 5g): her angry text, or her line when she is right there
# ============================================================
label _femdom_phone_order_no_show(girl):
    $ _fdo_line = femdom_phone_order_line(girl, "no_show")
    if getattr(girl, "loc", None) == CurrentLocation:
        $ Say_Line(girl, _fdo_line)
    else:
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Your phone buzzes. Someone sent you a message."))
        call _phone_typing(girl, choices=[]) from _femdom_phone_order_typing_no_show
        $ phone_add_msg(girl.gid, girl.gid, _tl(_fdo_line))
        call screen phone_chat_screen(girl, choices=[])
    $ femdom_request_refused(girl, "phone_order")
    return
