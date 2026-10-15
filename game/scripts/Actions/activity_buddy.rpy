# ============================================================
# ACTIVITY BUDDY SYSTEM
# Girls with specific traits invite the player to join activities.
# After enough shared sessions + sufficient Love, the girl texts
# the player asking to join her. Repeated attendance creates a
# routine that grants a small stat bonus.
# ============================================================

init python:

    # ── Trait → Activity mapping ──
    ACTIVITY_BUDDY_CONFIG = {
        "nerd": {
            "key": "study",
            "locations": frozenset({"classroom"}),
        },
        "gym_rat": {
            "key": "workout",
            "locations": frozenset({"gym"}),
        },
    }

    BUDDY_MIN_COUNT = 3
    BUDDY_ROUTINE_COUNT = 8
    BUDDY_LOVE_MIN = 350
    BUDDY_COOLDOWN_DAYS = 7
    BUDDY_CHANCE = 40

    # ── Invite dialogue pools ──

    BUDDY_INVITE_LINES = {
        "study": [
            _("Hey, I'm about to head to class. Want to come with me?"),
            _("I'm going to the classroom now. Join me?"),
            _("Want to sit with me in class today?"),
            _("Class is starting soon. Come study with me!"),
        ],
        "workout": [
            _("Heading to the gym right now. Need a workout buddy?"),
            _("I'm about to work out. You should come with me."),
            _("Gym time! Come spot me?"),
            _("About to hit the gym. You in?"),
        ],
    }

    BUDDY_INVITE_ROUTINE_LINES = {
        "study": [
            _("Same time as usual? I saved you a seat."),
            _("Class in five. Our usual spot?"),
            _("You know the drill. See you in class?"),
        ],
        "workout": [
            _("Same time as usual? The gym is calling."),
            _("Workout time. You already know."),
            _("Our usual gym session? I'm heading there now."),
        ],
    }

    BUDDY_ACCEPT_LINES = {
        "study": [
            _("Yes! It's always better with company."),
            _("Great! I'll save you a seat."),
            _("Awesome! See you there!"),
        ],
        "workout": [
            _("Nice! Let's do this!"),
            _("Great! See you there!"),
            _("Awesome! I'll be warming up, don't take too long!"),
        ],
    }

    BUDDY_DECLINE_LINES = [
        _("Oh... okay. Maybe next time then."),
        _("Alright, I guess I'll go alone."),
        _("That's fine. Another time, maybe."),
    ]

    # ── Femdom (docs/plan_femdom.md 7, "Convites"): her invite is an ORDER ──
    # Invite / accept: only once she is past her discovery phase (trait_is_veteran). While she is still discovering
    # the trait its voice stays silent (trait_line_keys) and the usual pools speak.
    # Decline: femdom_request_refused (she is angry, Obed down, never up) in any phase, with her angry line
    # instead of the usual decline reaction.

    BUDDY_INVITE_FEMDOM_LINES = {
        "study": [
            _("I'm going to class. You're coming with me. Move."),
            _("Classroom. Now. I'm not studying alone today."),
            _("You're sitting next to me in class today. That wasn't a question."),
        ],
        "workout": [
            _("Gym. Now. You're spotting me today."),
            _("I'm heading to the gym and you're coming. Don't make me wait."),
            _("Get to the gym. I need someone to push, and it's you."),
        ],
    }

    BUDDY_ACCEPT_FEMDOM_LINES = {
        "study": [
            _("Good. Don't make me wait."),
            _("Good boy. I'll save you a seat. Next to me, obviously."),
            _("Correct answer. Hurry up."),
        ],
        "workout": [
            _("Good. Warm up fast, I'm not waiting for you."),
            _("That's what I like to hear. Move."),
            _("Good boy. Try to keep up."),
        ],
    }

    BUDDY_DECLINE_FEMDOM_LINES = [
        _("Excuse me? That wasn't an invitation. It was an order."),
        _("Not this time? I don't remember giving you a choice."),
        _("Wrong answer. Remember this."),
    ]

    # Still discovering the trait: she finds out she hates hearing no (never an old habit)
    BUDDY_DECLINE_FEMDOM_NEW_LINES = [
        _("Oh. You said no... and I really didn't like hearing it. Huh."),
        _("Okay. Weird, I'm actually annoyed. I think I wanted you to just say yes."),
        _("Fine. But I'm finding out I hate being told no. Noted."),
    ]

    BUDDY_ACTIVITY_NARRATION = {
        "study": [
            _("You sit down and open your books together. The session flies by."),
            _("You focus on the lecture together. Time well spent."),
            _("She points out a few things you missed in the notes. Helpful as always."),
        ],
        "workout": [
            _("You push through the workout together. Good burn."),
            _("She keeps pace with you the whole session. Solid workout."),
            _("You spot each other through the sets. Feels like a real team effort."),
        ],
    }

    # ── Helper functions ──

    def _buddy_increment(girl, activity_key):
        if not hasattr(girl, "_buddy_activity_count"):
            girl._buddy_activity_count = {}
        girl._buddy_activity_count[activity_key] = girl._buddy_activity_count.get(activity_key, 0) + 1
        print("[BUDDY] %s %s count = %d" % (girl.gid, activity_key, girl._buddy_activity_count[activity_key]))

    def _buddy_is_routine(girl, activity_key):
        counts = getattr(girl, "_buddy_activity_count", {})
        return counts.get(activity_key, 0) >= BUDDY_ROUTINE_COUNT

    def _buddy_get_count(girl, activity_key):
        counts = getattr(girl, "_buddy_activity_count", {})
        return counts.get(activity_key, 0)

    def _activity_buddy_eligible(girl, day, time_index):
        if time_index == NIGHT_INDEX:
            return None

        if girl.loc == store.CurrentLocation:
            return None

        # the invite reads her SCHEDULE, not where she is: a girl giving birth would still ask him to study
        if girl_is_away(girl):
            return None

        if girl.gid not in getattr(store.Player, "phone_contacts", set()):
            return None

        if hasattr(girl, "has_temp_status") and (girl.has_temp_status("angry") or girl.has_temp_status("sad")):
            return None

        last_inv = getattr(girl, "_buddy_last_invite_day", 0)
        if last_inv > 0 and (day - last_inv) < BUDDY_COOLDOWN_DAYS:
            return None

        if girl.Love < BUDDY_LOVE_MIN:
            return None

        if hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
            return None

        dest = get_scheduled_location_for(girl, day, time_index)

        for trait, cfg in ACTIVITY_BUDDY_CONFIG.items():
            if not girl.has_trait(trait):
                continue
            if dest not in cfg["locations"]:
                continue
            count = _buddy_get_count(girl, cfg["key"])
            if count < BUDDY_MIN_COUNT:
                continue
            return cfg

        return None

    def _buddy_check_all():
        day = store.Day
        ti = store.TimeIndex
        candidates = girls_on_campus()   # a study / workout buddy on campus (never away, never off campus)
        renpy.random.shuffle(candidates)
        for girl in candidates:
            cfg = _activity_buddy_eligible(girl, day, ti)
            if cfg is None:
                continue
            if renpy.random.randint(1, 100) > BUDDY_CHANCE:
                print("[BUDDY] %s eligible for %s but failed roll" % (girl.gid, cfg["key"]))
                continue
            print("[BUDDY] %s will invite for %s" % (girl.gid, cfg["key"]))
            return (girl, cfg)
        return None


# ── Activity Buddy Invite (phone flow) ──

label _activity_buddy_invite(girl, buddy_cfg):

    $ _ab_key = buddy_cfg["key"]
    $ _ab_is_routine = _buddy_is_routine(girl, _ab_key)
    $ _ab_dest = get_scheduled_location_for(girl, Day, TimeIndex)
    # A veteran femdom doesn't invite, she orders (her discovery phase keeps the usual invite)
    $ _ab_femdom = trait_is_veteran(girl, "femdom")
    if _ab_femdom:
        $ print("[FEMDOM] %s buddy invite (%s) is an order" % (girl.gid, _ab_key))

    play sound "audio/Notification.mp3" noloop
    $ renpy.say(None, _tl(_("Your phone buzzes. Someone sent you a message.")))

    # Typing + message
    call _phone_typing(girl) from _typing_buddy_invite
    python:
        if _ab_femdom:
            _ab_msg = _tl(renpy.random.choice(BUDDY_INVITE_FEMDOM_LINES[_ab_key]))
        elif _ab_is_routine:
            _ab_msg = _tl(renpy.random.choice(BUDDY_INVITE_ROUTINE_LINES[_ab_key]))
        else:
            _ab_msg = _tl(renpy.random.choice(BUDDY_INVITE_LINES[_ab_key]))
        phone_add_msg(girl.gid, girl.gid, _ab_msg)

    # Accept / Decline
    python:
        _ab_choices = [
            (_tl(_("Sure, I'll be right there!")), "accept"),
            (_tl(_("Not this time.")), "decline"),
        ]
    call screen phone_chat_screen(girl, choices=_ab_choices)
    $ _ab_pick = _return

    if _ab_pick == "accept":
        $ phone_add_msg(girl.gid, "player", _tl(_("Sure, I'll be right there!")))

        call _phone_typing(girl) from _typing_buddy_accept
        python:
            _ab_accept_pool = BUDDY_ACCEPT_FEMDOM_LINES[_ab_key] if _ab_femdom else BUDDY_ACCEPT_LINES[_ab_key]
            _ab_accept_msg = _tl(renpy.random.choice(_ab_accept_pool))
            phone_add_msg(girl.gid, girl.gid, _ab_accept_msg)
        call screen phone_chat_screen(girl, auto_close=1.2, choices=[])

        # Record
        $ girl._buddy_last_invite_day = Day
        $ girl._buddy_accepted_count = getattr(girl, "_buddy_accepted_count", 0) + 1
        $ print("[BUDDY] %s invite accepted (day %d)" % (girl.gid, Day))

        # Navigate
        scene black
        with fade

        python:
            _ab_loc_name = _tl(LOC_NAMES.get(_ab_dest, _ab_dest))
            renpy.say(None, _tl(_("You head to %s to meet %s.")) % (_ab_loc_name, girl.Name))

        $ navigate_to(_ab_dest, None)
        call Set_Scene(entry=False) from _call_ab_set_scene

        # ── Inline activity effects ──

        $ _ab_narr = _tl(renpy.random.choice(BUDDY_ACTIVITY_NARRATION[_ab_key]))
        "[_ab_narr]"

        if _ab_key == "study":
            python:
                _study_gain = 4 if getattr(Player, "player_trait", "") == "fast_learner" else 2
                Player.study_level += _study_gain
                girl.study_level += (4 if girl.has_trait("nerd") else 2)
                Change_Status(girl, "Love", 3)
                _buddy_increment(girl, "study")

            $ renpy.say(None, _tl(_("Your study level: %d.")) % Player.study_level)

            if _buddy_is_routine(girl, "study"):
                $ Player.study_level += 1
                $ renpy.say(None, _tl(_("Studying with %s has become a routine. You learn faster together. {b}+1 Study Level{/b}.")) % girl.Name)

        elif _ab_key == "workout":
            python:
                _energy_gained = Player.register_workout()
                Change_Status(girl, "Love", 3)
                _buddy_increment(girl, "workout")

            if _energy_gained:
                $ renpy.say(None, _tl(_("All that hard work is paying off. You feel stronger. {b}Max Energy up!{/b} (Max Energy: %d/5)")) % Player.energy_max)

            if _buddy_is_routine(girl, "workout"):
                $ Change_Status(girl, "Love", 3)
                $ renpy.say(None, _tl(_("Working out with %s has become a routine. You push each other harder. {b}+3 Love{/b}.")) % girl.Name)

        # Consume remaining time in slot
        $ _ab_cost = max(1, 100 - Round)
        call Apply_Time_Cost(_ab_cost) from _call_ab_time_cost

        # Time advanced; inner Wait already processed the change.
        $ store._buddy_invite_accepted = True

    else:
        $ phone_add_msg(girl.gid, "player", _tl(_("Not this time.")))

        # He said no to her: a femdom girl is angry and loses Obed (femdom_request_refused, D1) instead of the usual
        # reaction (that one gives Obed: a femdom never gains Obed from asserting herself). On the femdom path
        # (she lost it to his refusals) it also counts toward the control corruption, and the usual reaction stays.
        $ _ab_angry = femdom_request_refused(girl, "invite")

        call _phone_typing(girl) from _typing_buddy_decline
        python:
            if _ab_angry:
                _ab_decline_pool = BUDDY_DECLINE_FEMDOM_NEW_LINES if trait_is_discovering(girl, "femdom") else BUDDY_DECLINE_FEMDOM_LINES
            else:
                _ab_decline_pool = BUDDY_DECLINE_LINES
            _ab_decline_msg = _tl(renpy.random.choice(_ab_decline_pool))
            phone_add_msg(girl.gid, girl.gid, _ab_decline_msg)
        call screen phone_chat_screen(girl, auto_close=1.2, choices=[])

        if not _ab_angry:
            $ Change_Status(girl, "Love", -5)
            $ Change_Status(girl, "Obed", 3)
        $ girl._buddy_last_invite_day = Day
        if _ab_angry:
            $ print("[BUDDY] %s invite declined: femdom, angry (femdom_request_refused)." % (girl.gid))
        else:
            $ print("[BUDDY] %s invite declined. Love -5, Obed +3." % (girl.gid))

    return
