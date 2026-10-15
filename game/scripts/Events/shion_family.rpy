# ============================================================
# shion_family.rpy... the player's family, off campus (docs/plan_shion.md, Fase 1 itens 4 a 6)
#
# THE FATHER (Dad): a FamilyContact with his own thread ("dad"), listed in Contacts after the girls
#   (family_contacts). In the apartment he is a man on the map with his own rooms, talk and stats (family_father.rpy);
#   dad_arrival_line tells where he is when the player arrives from campus. He is at work at Midday on weekdays (DAD_WORK_*),
#   and away on a business trip every DAD_TRIP_EVERY days for DAD_TRIP_DAYS days (dad_trip_daily, run by
#   _per_day_cleanup; texted the morning it starts and the morning after it ends).
# THE FIRST DINNER: he texts an invitation the first morning (_family_dinner "invited"), for the next Sunday at
#   least FAMILY_DINNER_MIN_DAYS away, a reminder that Sunday morning, and the dinner plays when the player is in
#   the apartment that Sunday Evening with her at home (apartment_event_now, from location_menu). Missed: his
#   text the next morning and a new invitation for the next Sunday. No business trip before the first dinner.
# THE SUNDAY DINNERS (docs/plan_role_situations.md, Fase 2): after the first one, he texts on Sunday morning for
#   that Evening (dad_morning_text "dinner_weekly", with "Not this week." as a way out) while a girl of the house has
#   the dinner on her story step (FAMILY_DINNER_STORY_EVENT, story_steps.rpy), he is home that Evening and the player
#   It plays like the first one (apartment_event_now "dinner_weekly"): her story picks what happens
#   at the table (story_event_now "dinner": her unlock event when a route passes, else her step's dinner). Missed:
#   his text the next morning (unless another text of his goes first).
# HER CURFEW: at Night the woman of the house (a girl who lives in the apartment, at home) sends him back to his
#   dorm room (label _apartment_curfew). Before she turns (Fase 3) it always happens.
# The family's girls (GIRLS_CONFIG "type": "family") are in his phone from the start (family_sync).
# All the father's texts: label _dad_text_event, Wait step 6zz2 (once per morning).
# ============================================================

init -1 python:

    class FamilyContact(object):
        """A family member who is not a Girl (the father): a phone contact with his own thread, and in the apartment a man
        with his own rooms (family_father.rpy). The phone screens read gid / Name / color; is_family tells him apart
        from a girl or an NPC partner; the roster shows him like an NPC (show_sprite / hide_sprite).
        Name translates at access time (_tr): "Dad" -> "Pai" in PT."""
        is_family = True

        def __init__(self, gid, name, color):
            self.gid = gid
            self._name_en = name
            self.color = color
            self.loc = None

        @property
        def Name(self):
            return _tr(self._name_en)

        def image_tag(self):
            return "family_%s" % self.gid

        def image_name(self):
            return "family_sprite_%s" % self.gid    # FAMILY_SPRITES (family_father.rpy)

        def show_sprite(self, transform):
            renpy.show(self.image_name(), tag=self.image_tag(), at_list=[transform], zorder=5)

        def hide_sprite(self):
            renpy.hide(self.image_tag())

default Dad = FamilyContact("dad", "Dad", "#94a3b8")
default _dad_trip = None                    # {"start": day, "end": day} of his business trip (both included), or None
default _dad_next_trip_day = 0              # the day his next trip starts (0 = not rolled yet)
default _dad_text_pending = None            # "trip_leave" / "trip_back": his text for the next morning
default _dad_trip_cut = False               # the trip was cut to end on Saturday: his text promises the Sunday dinner
default _family_dinner = "none"             # the first dinner: "none" -> "invited" (he texted) -> "done"
default _family_dinner_day = 0              # the Sunday he invited him for
default _family_dinner_reminded = False     # he already texted the reminder that Sunday morning
default _family_dinner_weekly_day = 0       # the Sunday of this week's dinner (he texted that morning), 0 = none
default _family_dinner_slot_ping = 0        # the Day his father's Evening "dinner's waiting" text went out (Wait 6m)

init python:

    DAD_WORK_WEEKDAYS = (1, 2, 3, 4, 5)     # Monday to Friday ((Day - 1) % 7, 0 = Sunday)
    DAD_WORK_SLOTS = (1,)                   # at work at Midday
    DAD_TRIP_EVERY = (10, 18)               # days from the end of one business trip to the start of the next
    DAD_TRIP_DAYS = (2, 4)                  # how long a trip lasts, in days
    FAMILY_DINNER_WEEKDAY = 0               # Sunday
    FAMILY_DINNER_SLOT = 2                  # Evening (arriving late, at Night, still counts: the trip takes time)
    FAMILY_DINNER_MIN_DAYS = 2              # an invitation is never for a Sunday closer than this
    APARTMENT_CURFEW = 3                    # from this time slot on (Night) she sends him back to campus
    FAMILY_DINNER_STORY_EVENT = "family_dinner"     # the Sunday dinners happen while a girl of the house has it on her step

    # Arriving from campus: what tells him where his father is (dad_where)
    # by the room he is in (dad_room, family_father.rpy), else "out" / "work" / "trip"
    DAD_ARRIVAL_LINES = {
        "apartment": [
            _("You hear the TV from the living room. Your father is home."),
            _("Your father's shoes are by the door. He's home."),
        ],
        "apartment_room": [
            _("Your father's voice comes from the bedroom. He's home."),
        ],
        "apartment_shower": [
            _("You hear the shower running. Your father is home."),
        ],
        "out": [
            _("The apartment is quiet. Your father went out."),
        ],
        "work": [
            _("The apartment is quiet. Your father is still at work."),
        ],
        "trip": [
            _("The apartment is quiet. Your father is away on his business trip."),
        ],
    }

    # His texts (label _dad_text_event). "%d" in trip_leave = the days he will be away.
    DAD_TEXTS = {
        "dinner_invite": [
            _("Hey kid. Shion and I want you over for dinner on Sunday. Evening, at the apartment."),
            _("It's time you two got to know each other properly. Don't make me beg."),
        ],
        "dinner_today": [
            _("Dinner tonight! Evening, at home. Shion ordered from that fancy place downtown."),
        ],
        "dinner_missed": [
            _("We waited for you last night, son. Shion wasn't happy."),
            _("Let's try again next Sunday, okay? Same time."),
        ],
        "dinner_weekly": [
            _("Family dinner tonight? Evening, at home. Shion picked the restaurant again."),
        ],
        "dinner_weekly_missed": [
            _("We saved you a plate last night, son. Shion threw it away."),
        ],
        "trip_leave": [
            _("Heading out on a business trip. I'll be back in %d days."),
            _("Stop by and keep Shion company if you can. The place is too quiet without me."),
        ],
        # appended to trip_leave when the span was cut to spare the Sunday dinner (_dad_trip_cut)
        "trip_leave_sunday": [
            _("Back Saturday, though. I wouldn't miss Sunday dinner."),
        ],
        "trip_back": [
            _("Back home! That trip was brutal. Come by sometime."),
        ],
        # the morning after she called him from his dorm too loudly (shion_netori.rpy)
        "netori_noise": [
            _("Shion sounded out of breath on the phone last night."),
            _("Is your dorm too hot or something? Make sure she's comfortable, kid."),
        ],
    }

    # His answer to "I'll be there." / "Do I have to?" (dinner_invite)
    DAD_DINNER_REPLY = {
        "yes": _("Good! She's looking forward to it."),
        "grumble": _("Yes. She's trying, son. Give her a chance."),
    }

    # His answer to "I'll be there." / "Not this week." (dinner_weekly)
    DAD_WEEKLY_REPLY = {
        "yes": _("Good! I'll tell Shion to set a plate."),
        "skip": _("Next week, then. Don't make it a habit."),
    }

    # She sends him away at Night (label _apartment_curfew)
    APARTMENT_CURFEW_LINES = [
        _("It's late, [Player.Name]. Go back to your dorm. Your father needs his rest."),
        _("Visiting hours are over. Go."),
        _("Don't you have a bed on campus? Use it."),
    ]

    def family_route_on():
        """The family household exists in this run: some family girl's optional route is on (girl_route_enabled,
        the stepmom's _stepmom_route). Off = no father on the map or phone, no dinner texts, no trips, and the
        Downtown crossroads hides the apartment."""
        return any(girl_type(_g) == "family" and girl_route_enabled(_g) for _g in ALL_GIRLS)

    def family_contacts():
        """The family members in his phone, after the girls (Contacts). Nobody with the route off."""
        return [store.Dad] if family_route_on() else []

    def family_sync(why):
        """New game and every load: a family girl whose route is OFF is out of his phone. Her number is
        NOT auto-added up front: she gives it when he asks (_ask_phone_number; her story's cold step
        refuses outright, story_act_locked "phone_number"), OR it saves itself the moment SHE texts him
        first (phone_add_msg, author 2026-10-11: her grade texts had no way to be answered).
        Old saves: the pre-2026-10-04 auto-added number leaves while she is on her cold step, UNLESS
        the chat holds a text of hers (then she texted him: the number is his by the new rule, and a
        save where the old migration already stripped it gets it back)."""
        _contacts = getattr(store.Player, "phone_contacts", None)
        if _contacts is None:
            return
        for _g in ALL_GIRLS:
            if girl_type(_g) != "family":
                continue
            if not girl_route_enabled(_g):
                if _g.gid in _contacts:
                    _contacts.discard(_g.gid)
                    print("[FAMILY] %s: %s route is off, her number left his phone" % (why, _g.gid))
                continue
            _she_texted = any(_m.get("sender") == _g.gid for _m in phone_get_msgs(_g.gid))
            if _she_texted and _g.gid not in _contacts:
                # migration (2026-10-11): she already texted him in this save, he could never answer
                _contacts.add(_g.gid)
                _g._number_from_her_text = True
                print("[FAMILY] %s: %s texted him before this rule, her number joined his phone" % (why, _g.gid))
            elif _g.gid in _contacts and story_first_step(_g) and not _she_texted:
                # migration (2026-10-04): the number used to be auto-added for family
                _contacts.discard(_g.gid)
                print("[FAMILY] %s: %s is still on her cold step, the auto-added number left his phone" % (why, _g.gid))

    # ── The father: where he is ──
    def dad_on_trip(day=None):
        _t = store._dad_trip
        _d = store.Day if day is None else day
        return bool(_t) and _t["start"] <= _d <= _t["end"]

    def dad_where(day=None, ti=None):
        """"trip" / "work" / "home": where the father is at that day and time slot (now by default)."""
        _d = store.Day if day is None else day
        _ti = store.TimeIndex if ti is None else ti
        if dad_on_trip(_d):
            return "trip"
        if (_d - 1) % 7 in DAD_WORK_WEEKDAYS and _ti in DAD_WORK_SLOTS:
            return "work"
        return "home"

    def father_is_home(day=None, ti=None):
        return dad_where(day, ti) == "home"

    def dad_arrival_line():
        """What tells him where his father is, when he arrives from campus (label Apartment_Arrive)."""
        _where = dad_where()
        _key = dad_room() or ("out" if _where == "home" else _where)
        return renpy.random.choice(DAD_ARRIVAL_LINES[_key])

    def dad_trip_daily():
        """_per_day_cleanup: his business trip starts or ends (the texts go out the same morning, Wait 6zz2).
        No trip before the first dinner (he would miss his own invitation)."""
        if not family_route_on():
            return
        _d = store.Day
        _t = store._dad_trip
        if _t and _d > _t["end"]:
            print("[DAD] back from his trip (Day %d to %d)" % (_t["start"], _t["end"]))
            store._dad_trip = None
            store._dad_text_pending = "trip_back"
            store._dad_next_trip_day = _d + renpy.random.randint(*DAD_TRIP_EVERY)
            print("[DAD] next trip on Day %d" % store._dad_next_trip_day)
            return
        if store._dad_next_trip_day <= 0:
            store._dad_next_trip_day = _d + renpy.random.randint(*DAD_TRIP_EVERY)
            print("[DAD] first trip on Day %d" % store._dad_next_trip_day)
            return
        if _t is None and _d >= store._dad_next_trip_day:
            # his wife is away giving birth (or about to): he stays (shion_pregnancy.rpy)
            if any(girl_is_away(_g) or getattr(_g, "_giving_birth", False) for _g in ALL_GIRLS if girl_husband(_g) is store.Dad):
                store._dad_next_trip_day = _d + 1
                print("[DAD] trip postponed to Day %d: his wife is giving birth" % store._dad_next_trip_day)
                return
            if store._family_dinner != "done":
                store._dad_next_trip_day = _d + 1
                print("[DAD] trip postponed to Day %d: the first dinner has not happened yet" % store._dad_next_trip_day)
                return
            _len = renpy.random.randint(*DAD_TRIP_DAYS)
            # The trip never covers a Sunday: the dinners need him home that Evening (a span over the
            # unlock dinner stalled her story for a week, tester 2026-10-10). Today Sunday = it waits for
            # Monday; a span that would reach Sunday ends on Saturday (his text says so: _dad_trip_cut).
            _ahead = (FAMILY_DINNER_WEEKDAY - (_d - 1) % 7) % 7
            if _ahead == 0:
                store._dad_next_trip_day = _d + 1
                print("[DAD] trip postponed to Day %d: Sunday dinner today" % store._dad_next_trip_day)
                return
            if _len > _ahead:
                print("[DAD] trip cut from %d to %d days: back for the Sunday dinner of Day %d" % (_len, _ahead, _d + _ahead))
                _len = _ahead
                store._dad_trip_cut = True
            store._dad_trip = {"start": _d, "end": _d + _len - 1}
            store._dad_text_pending = "trip_leave"
            print("[DAD] business trip: Day %d to %d (%d days)" % (_d, _d + _len - 1, _len))

    # ── The first dinner ──
    def family_dinner_next_sunday(day):
        """The Sunday of an invitation sent on `day`: the next one at least FAMILY_DINNER_MIN_DAYS away."""
        _ahead = (FAMILY_DINNER_WEEKDAY - (day - 1) % 7) % 7
        if _ahead < FAMILY_DINNER_MIN_DAYS:
            _ahead += 7
        return day + _ahead

    # ── The Sunday dinners ──
    def family_dinner_weekly_girl():
        """The girl of the house whose story step has the Sunday dinner on it (story_steps.rpy), or None."""
        for _g in girls_reachable():
            if girl_home_loc(_g) in APARTMENT_ROOMS and FAMILY_DINNER_STORY_EVENT in story_events_for(_g):
                return _g
        return None

    def family_dinner_weekly_due():
        """Sunday morning after the first dinner: he invites him for tonight (he is home tonight, the dinner is on for a
        girl of the house)."""
        return (store._family_dinner == "done" and (store.Day - 1) % 7 == FAMILY_DINNER_WEEKDAY
                and father_is_home(ti=FAMILY_DINNER_SLOT)
                and family_dinner_weekly_girl() is not None)

    def apartment_home_girl():
        """The girl who lives in the apartment and is at home right now (in one of its rooms), or None."""
        for _g in girls_reachable():
            if girl_home_loc(_g) in APARTMENT_ROOMS and _g.loc in APARTMENT_ROOMS:
                return _g
        return None

    def dad_morning_text():
        """Wait 6zz2 (once per morning): the key of his text this morning (DAD_TEXTS), or None. One text a
        morning: the dinner first (missed / today / the invitation), then a trip."""
        if not family_route_on():
            return None
        _st = store._family_dinner
        if _st == "invited" and store.Day > store._family_dinner_day:
            return "dinner_missed"
        if _st == "invited" and store.Day == store._family_dinner_day and not store._family_dinner_reminded:
            return "dinner_today"
        if _st == "none":
            return "dinner_invite"
        if store._dad_text_pending:
            return store._dad_text_pending
        # the Sunday dinners: yesterday's missed one (dropped after a day), today's invitation
        _wk = store._family_dinner_weekly_day
        if _wk and store.Day > _wk:
            if store.Day == _wk + 1:
                return "dinner_weekly_missed"
            store._family_dinner_weekly_day = 0
            print("[FAMILY] Sunday dinner of Day %d missed, his text dropped (another text went first)" % _wk)
            _wk = 0
        if not _wk and family_dinner_weekly_due():
            return "dinner_weekly"
        return None

    def apartment_curfew_girl():
        """At Night the woman of the house sends him back to campus: the girl who lives in the apartment, at
        home now, when he is in one of its rooms. None otherwise."""
        if store.TimeIndex < APARTMENT_CURFEW or store.CurrentLocation not in APARTMENT_ROOMS:
            return None
        _g = apartment_home_girl()
        # from that step of her STORY she lets him stay (FEMDOM_TURN_NO_CURFEW_STAGE; story_step, not femdom_stage:
        # losing the femdom trait past her final step must never bring the curfew back)
        if _g is not None and story_step(_g) >= FEMDOM_TURN_NO_CURFEW_STAGE:
            return None
        return _g

    def apartment_event_now():
        """location_menu: the family event that plays now in the apartment ("dinner" / "curfew", label
        _apartment_<key>), or None."""
        if store.CurrentLocation not in APARTMENT_ROOMS:
            return None
        if (store._family_dinner == "invited" and store.Day == store._family_dinner_day
                and store.TimeIndex >= FAMILY_DINNER_SLOT and apartment_home_girl() is not None):
            return "dinner"
        if (store._family_dinner == "done" and store._family_dinner_weekly_day == store.Day
                and store.TimeIndex >= FAMILY_DINNER_SLOT and apartment_home_girl() is not None and father_is_home()):
            return "dinner_weekly"
        if apartment_curfew_girl() is not None:
            return "curfew"
        return None


# ============================================================
# The father's texts (Wait 6zz2): the dinner invitation / reminder / missed dinner, his business trips
# ============================================================
label _dad_text_event(key):
    python:
        _dt_lines = list(DAD_TEXTS[key])
        if key == "trip_leave":
            _dt_days = (_dad_trip["end"] - _dad_trip["start"] + 1) if _dad_trip else DAD_TRIP_DAYS[0]
            _dt_lines[0] = _tl_fmt(_dt_lines[0], _dt_days)
            if store._dad_trip_cut:
                _dt_lines.append(DAD_TEXTS["trip_leave_sunday"][0])
                store._dad_trip_cut = False
        else:
            _dt_lines[0] = _tl(_dt_lines[0])
        _dt_lines[1:] = [_tl(_l) for _l in _dt_lines[1:]]
        print("[DAD] text '%s' (Day %d, dinner=%s on Day %d)" % (key, Day, _family_dinner, _family_dinner_day))

    play sound "audio/Notification.mp3" noloop
    $ Narration(_("Your phone buzzes. A message from your father."))

    while _dt_lines:
        call _phone_typing(Dad, choices=[]) from _dad_text_typing
        $ phone_add_msg(Dad.gid, Dad.gid, _dt_lines.pop(0))

    if key == "dinner_invite":
        python:
            store._family_dinner = "invited"
            store._family_dinner_day = family_dinner_next_sunday(Day)
            store._family_dinner_reminded = False
            print("[FAMILY] dinner invitation for Day %d" % store._family_dinner_day)
            _dt_choices = [(_tl(_("I'll be there.")), "yes"), (_tl(_("Do I have to?")), "grumble")]
        call screen phone_chat_screen(Dad, choices=_dt_choices)
        # his pick, kept: the typing call below sets _return to None (crashed with KeyError: None, 2026-10-06)
        $ _dt_pick = _return
        $ print("[FAMILY] dinner invitation: he answers %r" % (_dt_pick,))
        if _dt_pick in DAD_DINNER_REPLY:
            $ phone_add_msg(Dad.gid, "player", _dt_choices[0][0] if _dt_pick == "yes" else _dt_choices[1][0])
            call _phone_typing(Dad, choices=[]) from _dad_text_typing_reply
            $ phone_add_msg(Dad.gid, Dad.gid, _tl(DAD_DINNER_REPLY[_dt_pick]))
            call screen phone_chat_screen(Dad, choices=[])
    elif key == "dinner_weekly":
        python:
            store._family_dinner_weekly_day = Day
            print("[FAMILY] Sunday dinner invitation for tonight (Day %d)" % Day)
            _dt_choices = [(_tl(_("I'll be there.")), "yes"), (_tl(_("Not this week.")), "skip")]
        call screen phone_chat_screen(Dad, choices=_dt_choices)
        # his pick, kept: the typing call below sets _return to None (the same KeyError as the invitation)
        $ _dt_pick = _return
        $ print("[FAMILY] Sunday dinner text: he answers %r" % (_dt_pick,))
        if _dt_pick in DAD_WEEKLY_REPLY:
            python:
                phone_add_msg(Dad.gid, "player", _dt_choices[0][0] if _dt_pick == "yes" else _dt_choices[1][0])
                if _dt_pick == "skip":
                    store._family_dinner_weekly_day = 0
                    print("[FAMILY] he skips the Sunday dinner of Day %d" % Day)
            call _phone_typing(Dad, choices=[]) from _dad_text_typing_weekly
            $ phone_add_msg(Dad.gid, Dad.gid, _tl(DAD_WEEKLY_REPLY[_dt_pick]))
            call screen phone_chat_screen(Dad, choices=[])
    else:
        python:
            if key == "dinner_today":
                store._family_dinner_reminded = True
            elif key == "dinner_missed":
                store._family_dinner_day = family_dinner_next_sunday(Day)
                store._family_dinner_reminded = False
                print("[FAMILY] dinner missed: invited again for Day %d" % store._family_dinner_day)
            elif key == "dinner_weekly_missed":
                store._family_dinner_weekly_day = 0
                print("[FAMILY] Sunday dinner of Day %d missed" % (Day - 1))
            elif key == store._dad_text_pending:
                store._dad_text_pending = None
        call screen phone_chat_screen(Dad, choices=[])
    return

# ============================================================
# Contacts -> Dad -> Chat: his thread (nothing to send him yet)
# ============================================================
label family_phone_open_chat(who):
    $ store._phone_chat_exit = "back"
    call screen phone_chat_screen(who, choices=[])
    if _return == "home":
        $ store._phone_chat_exit = "home"
        $ _phone_restore_others()
    return

# ============================================================
# The first family dinner (location_menu, apartment_event_now "dinner"): the father introduces Shion
# ============================================================
label _apartment_dinner:
    python:
        _fd_her = apartment_home_girl()
        _fd_dad = Character(Dad.Name, who_color=Dad.color)
        store._family_dinner = "done"
        _fd_gf = next((_g for _g in ALL_GIRLS if _g is not _fd_her and _g.is_dating_player()), None)
        print("[FAMILY] the first dinner (Day %d): %s, his girlfriend=%s" % (Day, _fd_her.gid, getattr(_fd_gf, "gid", None)))
        _fd_her.loc = "apartment"
    if CurrentLocation != "apartment":
        $ navigate_to("apartment", None)
    call Set_Scene(entry=True) from _call_Set_Scene_family_dinner

    $ Narration(_("The table is set for three. Dinner is takeout from a restaurant you can't pronounce, served on plates that cost more than your whole dorm room."))
    $ renpy.say(_fd_dad, _tl(_("There he is! Sit, sit. Shion picked the place.")))

    $ set_scene_expression(_fd_her, "happy", pose="standing")
    $ Say_Line(_fd_her, _("Welcome home, [Player.Name]."))
    $ set_scene_expression(_fd_her, "sexy", pose="standing")
    $ Say_Line(_fd_her, _("Is something wrong, [Player.Name]? You look nervous."))

    menu:
        "I'm fine. Just hungry.":
            $ Say_Player(_("I'm fine. Just hungry."))
            $ set_scene_expression(_fd_her, "normal", pose="standing")
            $ Say_Line(_fd_her, _("Good. Then eat."))
            $ Change_Status(_fd_her, "Love", 2)
        "Should I be nervous?":
            $ Say_Player(_("Should I be nervous?"))
            $ set_scene_expression(_fd_her, "happy", pose="standing")
            $ Say_Line(_fd_her, _("Only if you've done something wrong. Have you?"))
            $ Change_Status(_fd_her, "Inbt", 3)
        "You're the one who looks nervous.":
            $ Say_Player(_("You're the one who looks nervous."))
            $ set_scene_expression(_fd_her, "sexy", pose="standing")
            $ Say_Line(_fd_her, _("Cute. Your father warned me you had a mouth on you."))
            $ Change_Status(_fd_her, "Love", -2)
            $ Change_Status(_fd_her, "Inbt", 5)

    $ renpy.say(_fd_dad, _tl(_("So, how's school? Still holding on to that scholarship?")))
    $ Say_Player(_("Still holding on."))
    $ set_scene_expression(_fd_her, "normal", pose="standing")
    $ Say_Line(_fd_her, _("Your father tells me three bad grades and it's gone."))
    $ Say_Line(_fd_her, _("So I'll see your grades every two weeks. Every exam."))
    $ Say_Line(_fd_her, _("My money pays for this apartment. Not for failures."))
    $ renpy.say(_fd_dad, _tl(_("She means she cares. Right, honey?")))
    $ set_scene_expression(_fd_her, "happy", pose="standing")
    $ Say_Line(_fd_her, _("Of course. He's family. My favorite investment."))

    if _fd_gf is not None:
        $ set_scene_expression(_fd_her, "normal", pose="standing")
        $ Say_Line(_fd_her, _tl_fmt(_("And this girl you're seeing, %s. We'll talk about her some other time."), _fd_gf.Name))

    $ Narration(_("The rest of dinner is your father talking about work, and Shion watching you over her wine glass."))
    $ renpy.say(_fd_dad, _tl(_("Come by anytime, son. This is your home too.")))
    $ set_scene_expression(_fd_her, "sexy", pose="standing")
    $ Say_Line(_fd_her, _("Anytime. Before dark."))
    $ set_scene_expression(_fd_her, "normal", pose="standing")

    # Her unlock fires at the FIRST dinner too (author 2026-10-11: with a route already passing, this
    # dinner played only the "everything is in place" nudge, which read as "nothing changed"). The
    # scripted introduction above plays first, then the table turns into her unlock, exactly as a
    # weekly dinner would. Only the UNLOCK: the step's own dinner moment (family_dinner) stays for
    # the weekly table, this script already was tonight's moment.
    python:
        _fd_ev = story_event_now("dinner", _fd_her)
        if _fd_ev is not None and _fd_ev[1] != story_unlock_event(_fd_her):
            _fd_ev = None
        print("[FAMILY] first dinner unlock check: %s" % (_fd_ev[1] if _fd_ev else "no route passing"))
    if _fd_ev is not None:
        call story_event_play(_fd_ev[0], _fd_ev[1]) from _call_story_event_first_dinner
        call _apartment_bus_home(_("The bus ride home is quiet. You keep replaying the dinner in your head.")) from _call_bus_home_first
    else:
        # no unlock tonight: what this one was missing (story_steps.rpy story_unlock_hint)
        call story_unlock_hint_say("dinner", _fd_her) from _call_story_hint_first_dinner

    # The dinner takes the rest of the evening (author 2026-10-11): he leaves the table into the
    # NIGHT, never into leftover evening rounds. Already Night (a late table): the old flat cost.
    python:
        _fd_cost = (NIGHT_INDEX - TimeIndex) * 100 - Round if TimeIndex < NIGHT_INDEX else 40
        print("[FAMILY] first dinner ends: TimeIndex=%d Round=%d -> cost %d (to Night)" % (TimeIndex, Round, _fd_cost))
    call Apply_Time_Cost(_fd_cost) from _call_Apply_Time_Cost_family_dinner
    if CurrentLocation == "room":
        # he went home by bus (_apartment_bus_home): his room at NIGHT on screen, not the street
        call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_set_scene_first_dinner_home
    return

# ============================================================
# A Sunday dinner (location_menu, apartment_event_now "dinner_weekly"): her story decides what happens at the table
# (story_steps.rpy: her unlock event "dinner" when a route passes, else her step's dinner)
# ============================================================
label _apartment_dinner_weekly:
    python:
        _fw_her = apartment_home_girl()
        store._family_dinner_weekly_day = 0
        _fw_her.loc = "apartment"
        _fw_ev = story_event_now("dinner", _fw_her)
        _fw_dad = girl_husband(_fw_her)
        _fw_dinners = story_data(STORY_DINNERS, _fw_her, {})
        print("[FAMILY] Sunday dinner (Day %d): %s, event %s, dad %s" % (Day, _fw_her.gid, _fw_ev[1] if _fw_ev else None, _fw_dad))
    if CurrentLocation != "apartment":
        $ navigate_to("apartment", None)
    call Set_Scene(entry=True) from _call_Set_Scene_family_dinner_weekly
    # main content: unlock event, step event, or quiet dinner
    if _fw_ev is not None:
        # save dad's roster slot before the event (to return him there later)
        python:
            _fw_dad_slot = slot_right
            if _fw_dad:
                _fw_roster = getattr(store, "_location_roster", None)
                _fw_near = _fw_roster.get("near", []) if _fw_roster else []
                if _fw_dad in _fw_near:
                    _fw_dad_slot = _get_slot_transform_for_index(_fw_near.index(_fw_dad), len(_fw_near))
        call story_event_play(_fw_ev[0], _fw_ev[1]) from _call_story_event_dinner
        if getattr(store, "_drugged_dinner_done", False):
            # the drugged dinner handled everything: no dad exit/return/dessert
            $ store._drugged_dinner_done = False
            # the narration says home, so he GOES home, and the trip is on screen (_apartment_bus_home)
            call _apartment_bus_home(_("You take the late bus home. Your head is somewhere else entirely.")) from _call_bus_home_drugged
        else:
            # after the event: dad slides off to the kitchen, private moment with her, dad returns for dessert
            python:
                _fw_step = story_step(_fw_her)
                _fw_dad_showing = _fw_dad and renpy.showing(_fw_dad.image_tag())
            if _fw_dad_showing:
                $ _fw_dad.show_sprite(witness_exit_left)
                pause 0.6
                $ _fw_dad.hide_sprite()
            call story_say(_fw_her, _fw_dinners.get("close", {}).get(_fw_step, [])) from _call_story_say_dinner_close_w
            python:
                _fw_ret = _fw_dinners.get("dad_return")
            if _fw_ret and _fw_dad:
                $ Narration(_tl(renpy.random.choice(_fw_ret)))
                $ _fw_dad.show_sprite(_fw_dad_slot)
            $ set_scene_expression(_fw_her, "normal", pose="standing")
            call story_say(_fw_her, _fw_dinners.get("dessert", {}).get(_fw_step, [])) from _call_story_say_dinner_dessert_w
            # The street-stand dessert (tester idea, 2026-10-10): the player baits him out, but only her
            # word moves him (family_wife_overrules) and only past her cold step. The window he leaves is
            # played inside her ladder (story_restricted_scene with the best act her step opens).
            if _fw_dad and renpy.showing(_fw_dad.image_tag()):
                menu:
                    # the caption says the PLAY, not just the line (the author 2026-10-11, tester: the old
                    # "Mention the dessert stand" read as small talk, not as a move to get him out of the house)
                    "Bait him out of the house: mention the dessert stand down the street":
                        $ Say_Player(_("You know what would top this off? Those desserts from the stand down the street."))
                        $ renpy.say(Character(_fw_dad.Name, who_color=_fw_dad.color), _tl(renpy.random.choice(FAMILY_DESSERT_REFUSE)))
                        python:
                            _fw_rules = family_wife_overrules(_fw_her) and not story_first_step(_fw_her)
                            _fw_win_act = next((_a for _a in ("sex", "bj", "hj") if story_act_open(_fw_her, _a)), None) if _fw_rules else None
                            print("[FAMILY] dessert run: %s overrules=%s, window act=%s (her step %s)" % (
                                _fw_her.gid, _fw_rules, _fw_win_act, story_step_id(_fw_her)))
                        if not _fw_rules:
                            $ set_scene_expression(_fw_her, "normal", pose="standing")
                            $ Say_Line(_fw_her, rod_pick_line(_fw_her, "family_dessert_backs_him"))
                        else:
                            $ set_scene_expression(_fw_her, "smug", pose="standing")
                            $ Say_Line(_fw_her, rod_pick_line(_fw_her, "family_dessert_order"))
                            $ renpy.say(Character(_fw_dad.Name, who_color=_fw_dad.color), _tl(renpy.random.choice(FAMILY_ERRAND_OBEY)))
                            python:
                                family_errand_out(_fw_dad)
                                _fw_dad.show_sprite(witness_exit_left)
                            pause 0.6
                            $ _fw_dad.hide_sprite()
                            $ Narration(_("The front door clicks shut. Three blocks there, a line at the stand, three blocks back."))
                            if _fw_win_act is not None:
                                call story_restricted_scene(_fw_her, _fw_win_act, "doggy" if _fw_win_act == "sex" else None) from _call_story_restricted_dessert
                            else:
                                # a ladder whose early steps open no act yet: the window is only tension
                                $ set_scene_expression(_fw_her, "sexy", pose="standing")
                                $ Narration(_("For a handful of minutes the two of you are alone, and she makes sure you feel every one of them."))
                            # he returns with the box; pinned to the living room for the rest of the slot
                            python:
                                _fw_dad._here = (Day, TimeIndex, "apartment")
                            $ Narration(_tl(renpy.random.choice(FAMILY_DESSERT_RETURN)))
                            $ _fw_dad.show_sprite(_fw_dad_slot)
                            $ set_scene_expression(_fw_her, "normal", pose="standing")
                    "Let the night wind down":
                        pass
            # the bus ride is real AND visible now: the street, the line, then his room (_apartment_bus_home)
            call _apartment_bus_home(_("The bus ride home is quiet. You keep replaying the dinner in your head.")) from _call_bus_home_weekly
    else:
        $ Narration(_("A quiet family dinner. Nobody says anything worth remembering."))
    # no unlock tonight: what was missing (none after an unlock: her next one is not a dinner)
    call story_unlock_hint_say("dinner", _fw_her) from _call_story_hint_dinner
    # The dinner takes the rest of the evening (author 2026-10-11): he leaves the table into the
    # NIGHT, never into leftover evening rounds. Already Night (a late table): the old flat cost.
    python:
        _fw_cost = (NIGHT_INDEX - TimeIndex) * 100 - Round if TimeIndex < NIGHT_INDEX else 40
        print("[FAMILY] Sunday dinner ends: TimeIndex=%d Round=%d -> cost %d (to Night)" % (TimeIndex, Round, _fw_cost))
    call Apply_Time_Cost(_fw_cost) from _call_Apply_Time_Cost_family_dinner_weekly
    if CurrentLocation == "room":
        # he went home by bus (_apartment_bus_home): his room at NIGHT on screen, not the street.
        # The quiet-dinner branch never left the apartment: the guard keeps its screen alone.
        call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_set_scene_weekly_dinner_home
    return

# ============================================================
# The late bus home that ends an apartment night (the dinners, the curfew): the street ON SCREEN,
# the ride narration, then his dorm room rendered. navigate_to alone draws nothing (author
# 2026-10-11: "The bus ride home" played with the apartment still on screen, and he stayed there
# visually). line None = no narration (the caller already said its goodbye).
# ============================================================
label _apartment_bus_home(line=None):
    scene expression ("bg downtown_night" if TimeIndex >= NIGHT_INDEX else "bg downtown")
    with fade
    if line:
        $ Narration(_tl(line))
    $ navigate_to("room", None)
    return

# ============================================================
# Her curfew (location_menu, apartment_event_now "curfew"): at Night she sends him back to his dorm
# ============================================================
label _apartment_curfew:
    python:
        _cf_her = apartment_curfew_girl()
        print("[FAMILY] curfew: %s sends him back to campus (Day %d, from %s)" % (_cf_her.gid, Day, CurrentLocation))
    if _cf_her.loc == CurrentLocation:
        $ set_scene_expression(_cf_her, "normal", pose="standing")
        $ Say_Line(_cf_her, renpy.random.choice(APARTMENT_CURFEW_LINES))
    else:
        # she is in another room: her voice through the wall
        $ Narration(_("You hear her voice from the other room."))
        $ Say_Line(_cf_her, renpy.random.choice(APARTMENT_CURFEW_LINES))
    $ Narration(_("You say goodnight and take the late bus back to your dorm."))
    # Her story (story_steps.rpy, "downtown_night"): what he sees on his way to the bus stop
    $ _story_dn = story_event_now("downtown_night", _cf_her)
    if _story_dn is not None:
        call story_event_play(_story_dn[0], _story_dn[1]) from _call_story_event_downtown_night
    # the goodbye was already spoken above: the street, then his room on screen
    call _apartment_bus_home(None) from _call_bus_home_curfew
    call Apply_Time_Cost(TIME_COSTS["navigate_apartment"]) from _call_Apply_Time_Cost_curfew
    if CurrentLocation == "room":
        call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_set_scene_curfew_home
    return
