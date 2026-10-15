init python:
    import random as _random
    from collections import defaultdict

    # ==========================================================
    # Hint highlight color (used by {hint}...{/hint} tag)
    # ==========================================================
    CHITCHAT_HINT_COLOR = "#6cb4ee"

    def _hint_tag(tag, argument, contents):
        return [(renpy.TEXT_TAG, "color=" + CHITCHAT_HINT_COLOR)] + contents + [(renpy.TEXT_TAG, "/color")]

    config.custom_text_tags["hint"] = _hint_tag

    # ==========================================================
    # Helpers
    # ==========================================================

 
    def get_sex_count(girl, key):
        """
        Safely read girl.Sex_acts[key] (acts with the player).
        Returns 0 if the dict or key does not exist.
        """
        # The attribute is Sex_acts: the old lowercase name never existed, so this always returned 0
        acts = getattr(girl, "Sex_acts", {}) or {}
        return acts.get(key, 0)

    # ==========================================================
    # Topic class + registry
    # ==========================================================

    _CHITCHAT_COND_ERRORS = set()   # ids of topics whose condition already logged an exception (init-time, never saved)

    class ChitChatTopic(object):
        """
        Represents a single chit-chat topic.

        func:      callable(girl, loc, t_index)
        condition: callable(girl, loc, t_index) -> bool
        weight:    numeric weight used for random selection
        """
        def __init__(self, func, condition=None, weight=1, student=False):
            self.func = func
            self.condition = condition or (lambda g, loc, t: True)
            self.weight = weight
            self.student = student

        def is_available(self, girl, loc, t_index):
            """
            Returns True if this topic can run in the current context.
            Any error in condition will be treated as 'not available'.
            A student topic (classes, professors, dorm life...) never runs for a girl who is not a student (Shion).
            """
            if self.student and girl_type(girl) != "student":
                return False
            try:
                return self.condition(girl, loc, t_index)
            except Exception as _e:
                # a typo in a condition used to kill its topic without a trace: say it once per topic
                if id(self) not in _CHITCHAT_COND_ERRORS:
                    _CHITCHAT_COND_ERRORS.add(id(self))
                    print("[CHITCHAT] condition of topic '%s' raised %r: the topic is unavailable" % (getattr(self.func, "__name__", "?"), _e))
                return False

    # _CHITCHAT_TOPICS["global"]  -> global topics available to all girls
    # _CHITCHAT_TOPICS["frieren"] -> Frieren-specific topics
    # _CHITCHAT_TOPICS["gwen"]    -> Gwen-specific topics
    # Underscore prefix: lambdas in conditions break pickle/save
    _CHITCHAT_TOPICS = defaultdict(list)

    def register_chitchat(gid, func, condition=None, weight=1, student=False):
        """
        Register a chit-chat topic.

        gid:
        - "global" for topics available to all girls
        - or girl.gid in lowercase, e.g. "frieren", "gwen"
        func:
        - function with signature func(girl, loc, t_index)
        condition:
        - optional callable(girl, loc, t_index) -> bool
        weight:
        - relative chance of this topic being selected
        student:
        - True = a student's topic (classes, professors, dorm life): only for a girl whose type is "student"
        """
        _CHITCHAT_TOPICS[gid.lower()].append(
            ChitChatTopic(func, condition=condition, weight=weight, student=student)
        )

    # Per-girl queue to avoid repeating topics before all others are played.
    # Uses underscore prefix to avoid Ren'Py save/pickle issues.
    store._chitchat_queues = {}

    # Functions that use renpy.display_menu() — unsafe for phone mode
    _CHITCHAT_HAS_MENU = set()

    def pick_chitchat_func(girl, loc, t_index):
        """
        Build the topic pool from:
        - global topics
        - girl-specific topics (based on girl.gid)
        Filter by condition, then pick one using weighted random.
        Uses a per-girl queue so every topic plays before any repeats.
        Returns a function: func(girl, loc, t_index)
        """
        gid = getattr(girl, "gid", "").lower()

        topics = []
        topics.extend(_CHITCHAT_TOPICS.get("global", []))
        topics.extend(_CHITCHAT_TOPICS.get(gid, []))

        # Filter by condition; a girl with a story keeps only the global topics of her step (story_global_topic_ok)
        _globals = set(id(t) for t in _CHITCHAT_TOPICS.get("global", []))
        available = [t for t in topics if t.is_available(girl, loc, t_index)
                     and (id(t) not in _globals or story_global_topic_ok(girl, t.func))]

        # Phone mode: exclude topics with interactive menus
        if getattr(store, "_phone_mode", False):
            available = [t for t in available if t.func not in _CHITCHAT_HAS_MENU]

        if not available:
            return chitchat_fallback_generic

        # Get or create the girl's queue (set of topic ids still unplayed)
        queue = store._chitchat_queues.get(gid, None)
        available_ids = set(id(t) for t in available)

        # Filter queue to only topics still available this call
        if queue is not None:
            queue = queue & available_ids
        # If queue empty or not yet created, reset to all available
        if not queue:
            queue = set(available_ids)

        # Weighted pick from queued topics only
        queued = [t for t in available if id(t) in queue]
        total = sum(t.weight for t in queued)
        r = renpy.random.uniform(0, total)
        acc = 0.0
        chosen = queued[0]
        for t in queued:
            acc += t.weight
            if r <= acc:
                chosen = t
                break

        # Remove chosen from queue
        queue.discard(id(chosen))
        store._chitchat_queues[gid] = queue

        return chosen.func

    # ==========================================================
    # TOPIC FUNCTIONS
    # ==========================================================
    # All topic functions must follow this signature:
    #   def func(girl, loc, t_index): ...

    # ---------- GLOBAL (COLLEGE SLICE-OF-LIFE) ----------

    def chitchat_global_study_reminder(girl, loc, t_index):
        _dte = days_until_exam(store.Day) if hasattr(store, "Day") else 7

        if _dte > 5:
            # Relaxed... exam is far away
            _reminder_lines = [
                _("The exam is still a while away, but don't let that fool you."),
                _("We've got time before the next test. Just don't waste it all."),
                _("The exam isn't soon, but it sneaks up faster than you think."),
            ]
            set_scene_expression(girl, "normal")
            Say_Line(girl, _tl(renpy.random.choice(_reminder_lines)))

            _followup = [
                _("Might be a good idea to start reviewing early for once."),
                _("A little bit each day goes a long way, you know?"),
                _("Let's not be the ones cramming the night before."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_followup)))
        elif _dte > 2:
            # Getting closer
            _reminder_lines = [
                _("The exam is getting closer... have you started preparing?"),
                _("We don't have that many days left before the test."),
                _("The exam is coming up. Don't wait until the last minute."),
            ]
            set_scene_expression(girl, "worried")
            Say_Line(girl, _tl(renpy.random.choice(_reminder_lines)))

            _followup = [
                _("Seriously, start reviewing if you haven't already."),
                _("I'd rather not see you panic the night before."),
                _("Let's both make sure we're ready, okay?"),
            ]
            set_scene_expression(girl, "normal")
            Say_Line(girl, _tl(renpy.random.choice(_followup)))
        else:
            # Urgent... exam very soon
            _reminder_lines = [
                _("The exam is practically tomorrow! Are you ready?"),
                _("We barely have any time left before the test!"),
                _("The exam is right around the corner... please tell me you studied."),
            ]
            set_scene_expression(girl, "angry")
            Say_Line(girl, _tl(renpy.random.choice(_reminder_lines)))

            _followup = [
                _("If you haven't studied yet, now is your last chance."),
                _("I'm stressed just thinking about it..."),
                _("We need to buckle down. No more excuses."),
            ]
            set_scene_expression(girl, "sad")
            Say_Line(girl, _tl(renpy.random.choice(_followup)))

        # Tease line... only if stats are high
        _love = getattr(girl, "Love", 0)
        _inbt = getattr(girl, "Inbt", 0)
        if max(_love, _inbt) >= 300:
            _tease_lines = [
                _("If you fail, I'll tease you first and help you after."),
                _("You better pass... or I'll have to punish you my way."),
                _("Fail and I get to make fun of you. Deal?"),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_tease_lines)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_global_teacher_gossip(girl, loc, t_index):
        _set_standing_arm(girl, 3)
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Have you noticed that teacher who disappears half the class?"))
        _set_standing_arm(girl, 2)
        set_scene_expression(girl, "angry")
        Say_Line(girl, _("They're either hiding something or just addicted to some game."))
        _set_standing_arm(girl, 0)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_too_late_to_study(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("It's probably too late to start studying today, right?"))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("We can panic together tomorrow instead."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_fallback_generic(girl, loc, t_index):
        _openers = [
            _("So, how's your day going?"),
            _("So... anything interesting happen today?"),
            _("Hey. You look like you've been thinking about something."),
            _("Random thought, but have you ever just sat here and watched people walk by?"),
        ]
        _followups = [
            _("Nothing special? Yeah, same here."),
            _("It's one of those days, huh? I get it."),
            _("Sometimes quiet days are the best ones."),
            _("Well, at least we're hanging out. That counts for something."),
        ]
        _set_standing_arm(girl, renpy.random.choice([1, 3]))
        set_scene_expression(girl, "normal")
        Say_Line(girl, _tl(renpy.random.choice(_openers)))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_followups)))
        _set_standing_arm(girl, 0)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    # Her own answer to "what are you up to?" at a place where the generic one below is not true for her (a woman who
    # is not a student: her home, the mall). gid -> place -> {"face", "lines"[, "phone"]}: "lines" are said face to
    # face; "phone" is what she texts from there when the "lines" need him in the room with her. A girl or a place
    # missing here keeps the generic answers.
    # How she hands the question back after her answer (chitchat_whats_up): gid -> (face, lines). Shion is not glad
    # he came to find her.
    _WHATS_UP_HOOKS = {
        "shion": ("smirk", [
            _("Well? Don't just stand there. Say something worth my time."),
            _("And you? I hope it's something your father would be proud of."),
            _("Your turn. Impress me."),
        ]),
    }

    _WHATS_UP_OWN = {
        # Shion lives in the father's apartment (docs/plan_shion.md): it's HER home, he is the one who has to explain
        "shion": {
            "apartment": {"face": "smirk", "lines": [
                _("I live here, [Player.Name]. The better question is what YOU are doing here."),
                _("Going over reports from the office, because nobody there can think without me. Now. What are YOU doing here?"),
            ], "phone": [
                _("Working from home. Reports, numbers, incompetent people. The usual."),
                _("Sitting in my living room, reading a report nobody else at that company understands."),
            ]},
            "apartment_room": {"face": "annoyed", "lines": [
                _("This is my bedroom, [Player.Name]. What exactly are YOU doing in it?"),
                _("Resting. I was, anyway. Do you always walk into a woman's bedroom like you own it?"),
            ], "phone": [
                _("Resting in my room. Alone, and I'd like to keep it that way for a while."),
                _("Going through my calendar. It's full. It's always full."),
            ]},
            "apartment_shower": {"face": "annoyed", "lines": [
                _("This is my bathroom, [Player.Name]. What are YOU doing in it?"),
                _("Getting ready. Perfection takes time, and you're wasting mine."),
            ], "phone": [
                _("Getting ready. Hair, skin, nails. Perfection takes time."),
            ]},
            # on her schedule, not window shopping between classes
            "mall": {"face": "smug", "lines": [
                _("Shopping. Unlike the girls on your campus, I actually buy what I try on."),
                _("Picking up a few things. A dress, a watch, new shoes. The staff here get nervous when they see me coming."),
            ]},
        },
    }

    def _whats_up_answer(girl, loc, t_index):
        """Pick a grounded 'what she's doing' answer based on where she is + the time.
        Over the phone `loc` is where HE is: the answer is about where SHE is (girl.loc).
        Returns (expression, list_of_lines)."""
        _phone = getattr(store, "_phone_mode", False)
        _l = ((getattr(girl, "loc", None) if _phone else loc) or loc or "").lower()
        _is_room = _l == "room" or _l.endswith("_room")
        _morning = t_index == 0
        _evening = t_index == 2
        _night = t_index >= 3

        _own = _WHATS_UP_OWN.get(getattr(girl, "gid", ""), {}).get(_l)
        if _own:
            _pool = (_own.get("phone") or _own["lines"]) if _phone else _own["lines"]
            print("[CHITCHAT] whats_up: %s answers at %s with her own lines (%s)" % (girl.gid, _l, "phone" if _phone else "face to face"))
            return _own["face"], _pool
        if _l in APARTMENT_ROOMS and girl_home_loc(girl) not in APARTMENT_ROOMS:
            # a guest in the father's apartment (she came with him): not her room, not her bathroom
            print("[CHITCHAT] whats_up: %s is a guest at %s" % (girl.gid, _l))
            if _l == "apartment_room":
                return "shy", [
                    _("Snooping a little. Relax, I didn't open any drawers."),
                    _("Admiring the bed. It's bigger than my whole room."),
                ]
            if _l == "apartment_shower":
                return "shy", [
                    _("Just freshening up. This bathroom is fancier than most hotels."),
                    _("Trying out the fancy shower while I can. Don't tell anyone I used the expensive soap."),
                ]
            return "smile", [
                _("Just looking around. This place is way nicer than anything on campus."),
                _("Trying not to touch anything. Everything in here looks like it costs more than everything I own."),
            ]

        if _l == "gym":
            return "smile", [
                _("Just finished a set. Give me a sec, I'm still catching my breath."),
                _("Getting a workout in before the motivation runs out. It doesn't last long."),
                _("Between sets, honestly. You caught me on a break."),
            ]
        if _l == "pool":
            if _evening or _night:
                return "smile", [
                    _("Just floating around. The pool's so much nicer once everyone leaves."),
                    _("Cooling off. It's the only quiet I get all day."),
                ]
            return "smile", [
                _("Working on my tan and ignoring everything I'm supposed to be doing."),
                _("Just here to feel the sun and not think for a while."),
            ]
        if _l == "classroom":
            if _morning:
                return "sad", [
                    _("Trying to wake up before class actually starts. Not going great."),
                    _("Pretending I did the reading. You know how it is."),
                ]
            return "normal", [
                _("Killing time between classes. This room makes me sleepy."),
                _("Waiting for the next lecture and dreading it a little."),
            ]
        if _l == "mall":
            return "smile", [
                _("Just browsing. I never actually buy anything, it's more of a hobby."),
                _("Window shopping. If I don't try things on, it doesn't count as spending, right?"),
            ]
        if _l == "shower" or _l in SHOWER_SPOTS:
            return "shy", [
                _("Just freshening up. You've got timing, I'll give you that."),
                _("Rinsing off after the day. Give a girl a little warning next time."),
            ]
        if _is_room:
            if _night:
                return "normal", [
                    _("Winding down for the night. My brain's already clocked out."),
                    _("Just relaxing in bed. This is the best part of the day, honestly."),
                ]
            return "smile", [
                _("Hiding in my room, mostly. Recharging before I have to be a person again."),
                _("Not much. Just me, some music, and zero responsibilities for five minutes."),
            ]
        # campus / default
        if _morning:
            return "normal", [
                _("Just got here, honestly. Still halfway asleep."),
                _("Figuring out my day. It's not off to a strong start."),
            ]
        if _night:
            return "smile", [
                _("Was about to head off, actually. But I've got a minute for you."),
                _("Just enjoying how quiet it gets out here at night."),
            ]
        return "normal", [
            _("Nothing set in stone. Kind of just seeing where the day takes me."),
            _("Between things. I was hoping something more interesting would come up... and here you are."),
        ]

    def chitchat_whats_up(girl, loc, t_index):
        """Player actually asks what she's up to; she answers based on context."""
        _openers = [
            _("So, what are you up to?"),
            _("Hey. What are you in the middle of?"),
            _("What's keeping you busy right now?"),
        ]
        _set_standing_arm(girl, 1)
        set_scene_expression(girl, "normal")
        Say_Player(renpy.random.choice(_openers))

        _expr, _answers = _whats_up_answer(girl, loc, t_index)
        _set_standing_arm(girl, 3)
        set_scene_expression(girl, _expr)
        Say_Line(girl, _tl(renpy.random.choice(_answers)))

        _hooks = [
            _("What about you? You look like you're up to something."),
            _("Anyway. I'm glad you came to find me."),
            _("You? Please tell me you've got something more exciting going on."),
        ]
        # her own way of handing the question back (_WHATS_UP_HOOKS), else the shared one
        _hook_face, _hooks = _WHATS_UP_HOOKS.get(girl.gid, ("smile", _hooks))
        set_scene_expression(girl, _hook_face)
        Say_Line(girl, _tl(renpy.random.choice(_hooks)))
        _set_standing_arm(girl, 0)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    # ==========================================================
    # Early-game chitchats (introductions, low stats)
    # ==========================================================

    def chitchat_first_introduction(girl, loc, t_index):
        """First real conversation. They recognize each other from class."""
        _is_shy = girl.has_trait("public_shy") if hasattr(girl, "has_trait") else False

        if _is_shy:
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("Um... h-hey. I think we're in the same class? Academic writing?"))
            set_scene_expression(girl, "normal", blush=1)
            Say_Line(girl, _("Sorry, I'm not great at this... what was your name again?"))
        else:
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Hey, I know you! We're in academic writing together, right?"))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("So... what's your name again? I'm terrible with names."))

        _name = girl.Name
        choices = [
            (_tl(_("Hey, I remember you too, %s, right? I'm [Player.Name].")) % _name, "love"),
            (_tl(_("You sure you don't remember? I could never forget yours, %s.")) % _name, "obed"),
            (_tl(_("[Player.Name]. You're going to get used to saying that a lot.")), "inbt"),
        ]
        result = renpy.display_menu(choices)

        if result == "love":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Yeah, that's me! Nice to properly meet you, [Player.Name]."))
            Change_Status(girl, "Love", 5)
        elif result == "obed":
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("Oh... that's... that's really sweet, actually."))
            Change_Status(girl, "Obed", 5)
            Change_Status(girl, "Love", 2)
        elif result == "inbt":
            set_scene_expression(girl, "surprise")
            Say_Line(girl, _("Wow, confident much? ...I kinda like it though."))
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Love", 2)

        girl.set_flag("introduced_to_player", True)

    def chitchat_what_do_you_do(girl, loc, t_index):
        """Early conversation about campus activities."""
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("So, [Player.Name], what do you usually do around campus? Like, outside of class."))

        choices = [
            (_("I hit the gym a lot. Gotta stay in shape."), "gym"),
            (_("I like to swim. The pool here is pretty nice."), "swim"),
            (_("Honestly? I study. A lot."), "study"),
        ]
        result = renpy.display_menu(choices)

        if result == "gym":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Oh, so that explains... well. Yeah, the gym here is nice!"))
            Change_Status(girl, "Obed", 3)
            Change_Status(girl, "Love", 2)
        elif result == "swim":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("The pool is great! I go there sometimes too. Maybe I'll see you around."))
            Change_Status(girl, "Inbt", 3)
            Change_Status(girl, "Love", 2)
        elif result == "study":
            set_scene_expression(girl, "surprise")
            Say_Line(girl, _("Wow, dedicated. That's actually really impressive. Most guys here just mess around."))
            Change_Status(girl, "Love", 5)

        girl.set_flag("asked_campus_activity", True)

    def chitchat_player_hobby(girl, loc, t_index):
        """Player shares a hobby. 5 options, 3 shown randomly. Trait compatibility bonus."""
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("I feel like I barely know anything about you. What do you do for fun?"))

        _all_hobbies = [
            (_("I'm into amateur photography. I like capturing the moment."), "photo"),
            (_("I work out as hard as I can. Pushing my limits is my thing."), "workout"),
            (_("I read a lot. Books, articles, anything really."), "reading"),
            (_("Swimming. It clears my head."), "swimming"),
            (_("Nothing special, just scrolling my phone honestly."), "phone"),
        ]
        renpy.random.shuffle(_all_hobbies)
        _choices = _all_hobbies[:3]
        result = renpy.display_menu(_choices)

        _has_t = hasattr(girl, "has_trait") and girl.has_trait

        if result == "photo":
            _bonus = _has_t and (girl.has_trait("camera_lover") or girl.has_trait("exhibitionist"))
            if _bonus:
                _set_standing_arm(girl, 3)
                set_scene_expression(girl, "shy")
                Say_Line(girl, _("Photography? That's... actually really cool. I've always thought cameras can be... exciting."))
                Change_Status(girl, "Love", 4)
                Change_Status(girl, "Obed", 3)
                if girl.has_trait("camera_lover"):
                    girl.discover("discovered_trait_camera_lover")
                if girl.has_trait("exhibitionist"):
                    girl.discover("discovered_trait_exhibitionist")
            else:
                set_scene_expression(girl, "smile")
                Say_Line(girl, _("Oh, that's a nice hobby! You any good?"))
                Change_Status(girl, "Love", 3)

        elif result == "workout":
            _bonus = _has_t and girl.has_trait("hardcore_sex")
            if _bonus:
                _set_standing_arm(girl, 3)
                set_scene_expression(girl, "smile")
                Say_Line(girl, _("A guy who pushes himself to the limit? ...I can respect that. A lot."))
                Change_Status(girl, "Love", 3)
                Change_Status(girl, "Inbt", 4)
            else:
                set_scene_expression(girl, "normal")
                Say_Line(girl, _("That's cool. Staying active is important, I guess."))
                Change_Status(girl, "Love", 2)

        elif result == "reading":
            _bonus = _has_t and (girl.has_trait("public_shy") or girl.has_trait("cute_sex"))
            if _bonus:
                set_scene_expression(girl, "shy")
                Say_Line(girl, _("You read? That's so... I love that. Most people don't have the patience for it anymore."))
                Change_Status(girl, "Love", 5)
                Change_Status(girl, "Obed", 2)
            else:
                set_scene_expression(girl, "smile")
                Say_Line(girl, _("Reading, huh? That's pretty chill. Any recommendations?"))
                Change_Status(girl, "Love", 3)

        elif result == "swimming":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Swimming is nice. Very... relaxing. And healthy!"))
            Change_Status(girl, "Love", 2)

        elif result == "phone":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Ha, same honestly. At least you're honest about it."))
            Change_Status(girl, "Love", 1)

        girl.set_flag("shared_hobby", True)

    def chitchat_do_you_work_out(girl, loc, t_index):
        """She asks if the player works out. Leads to gym/fitness talk."""
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Hey, random question... do you work out?"))

        choices = [
            (_("Yeah, I try to go to the gym regularly."), "yes"),
            (_("Sometimes. When I feel like it."), "sometimes"),
            (_("Not really. Why, do I look like I should?"), "no"),
        ]
        result = renpy.display_menu(choices)

        if result == "yes":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("I could tell. I mean... not in a weird way! You just look... healthy."))
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("...Anyway! If you ever want a gym buddy, let me know."))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Obed", 2)
        elif result == "sometimes":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Fair enough. It's hard to stay motivated when you're doing it alone."))
            Say_Line(girl, _("Maybe having someone to go with would help?"))
            Change_Status(girl, "Love", 2)
            Change_Status(girl, "Inbt", 2)
        elif result == "no":
            set_scene_expression(girl, "surprise")
            Say_Line(girl, _("What? No! I was just curious!"))
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("...But you know, the gym here is pretty good. Just saying."))
            Change_Status(girl, "Inbt", 3)

        girl.set_flag("asked_workout", True)

    def chitchat_have_a_girlfriend(girl, loc, t_index):
        """She asks if the player has a girlfriend."""
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("So... and this is just me being curious... do you have a girlfriend?"))

        choices = [
            (_("Nope. Single."), "single"),
            (_("It's complicated."), "complicated"),
            (_("Why, are you interested?"), "flirt"),
        ]
        result = renpy.display_menu(choices)

        if result == "single":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Oh! Cool. I mean, not cool that you're alone or anything! Just... good to know."))
            Change_Status(girl, "Love", 3)
        elif result == "complicated":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Ah... complicated. I get it. Relationships are messy sometimes."))
            Change_Status(girl, "Love", 2)
            Change_Status(girl, "Inbt", 2)
        elif result == "flirt":
            _set_standing_arm(girl, 3)
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("W-What?! I was just making conversation!"))
            _set_standing_arm(girl, 0)
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("...But I didn't say no."))
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Love", 2)

        girl.set_flag("asked_girlfriend", True)

    def chitchat_first_impression(girl, loc, t_index):
        """She mentions she noticed the player before."""
        _set_standing_arm(girl, 3)
        set_scene_expression(girl, "shy")
        Say_Line(girl, _("Can I be honest? I actually noticed you before we started talking."))
        _set_standing_arm(girl, 0)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Not in a creepy way! You just... stand out, I guess."))

        choices = [
            (_("I noticed you too, actually."), "mutual"),
            (_("Really? I had no idea."), "oblivious"),
            (_("Hard not to notice someone like you."), "bold"),
        ]
        result = renpy.display_menu(choices)

        if result == "mutual":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("You did? That makes me feel a lot less awkward about saying it."))
            Change_Status(girl, "Love", 5)
        elif result == "oblivious":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Typical. Guys never notice until you spell it out for them."))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Well, you know now."))
            Change_Status(girl, "Inbt", 3)
            Change_Status(girl, "Love", 2)
        elif result == "bold":
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("I... okay, that one caught me off guard."))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("You're trouble, aren't you?"))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Obed", 3)

        girl.set_flag("first_impression_chat", True)

    def chitchat_eat_together(girl, loc, t_index):
        """She suggests eating together."""
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Hey, you eaten yet? I was thinking about grabbing something from the cafeteria."))

        choices = [
            (_("Sure, let's go!"), "yes"),
            (_("Maybe, if I don't have anything else going on."), "maybe"),
            (_("Just the two of us?"), "flirty"),
        ]
        result = renpy.display_menu(choices)

        if result == "yes":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Great! I hate eating alone. Come on, let's go."))
            Change_Status(girl, "Love", 4)
        elif result == "maybe":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Wow, playing hard to get with cafeteria food? Bold strategy."))
            Change_Status(girl, "Love", 2)
        elif result == "flirty":
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("I mean... yeah? Unless you want me to invite the whole campus."))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Come on, it's just lunch."))
            Change_Status(girl, "Inbt", 4)
            Change_Status(girl, "Love", 2)

        girl.set_flag("ate_together", True)

    def chitchat_you_look_different(girl, loc, t_index):
        """She comments on the player's appearance/mood."""
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Hey... something about you is different today. Did you change something?"))

        choices = [
            (_("You look great too, by the way."), "compliment"),
            (_("Different how?"), "curious"),
            (_("Didn't sleep well, honestly."), "vulnerable"),
        ]
        result = renpy.display_menu(choices)

        if result == "compliment":
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("I wasn't fishing for compliments! But... thank you."))
            Change_Status(girl, "Love", 4)
            Change_Status(girl, "Inbt", 2)
        elif result == "curious":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("I don't know... you seem more confident? Or maybe I'm just paying more attention."))
            Change_Status(girl, "Love", 3)
        elif result == "vulnerable":
            set_scene_expression(girl, "sad")
            Say_Line(girl, _("Oh no... want to talk about it? Or we can just hang out, no pressure."))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Obed", 3)

    def chitchat_talked_to_others(girl, loc, t_index):
        """She asks if the player has talked to anyone else on campus.
        Shows other available girls as choices + 'only you' option.
        If a girl is picked, gives a friendship hint about their relationship."""
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("So, have you been talking to anyone else around here? Or am I your only friend?"))

        # Build list of other girls the player has already introduced to
        _others = []
        for _og in ALL_GIRLS:
            if _og.gid == girl.gid:
                continue
            if not hasattr(_og, "Name"):
                continue
            if _og.get_flag("introduced_to_player"):
                _others.append(_og)

        # Build menu choices
        _choices = []
        for _og in _others:
            _choices.append((_tl(_("I've been talking to %s.")) % _og.Name, _og.gid))
        _choices.append((_("Actually, only you."), "only_you"))

        result = renpy.display_menu(_choices)

        if result == "only_you":
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("Really? Just me? That's... kind of sweet, actually."))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("Well, I'm not complaining. More of your attention for me."))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 2)
        else:
            # Player picked another girl
            _picked = GIRL_BY_ID.get(result)
            if _picked and hasattr(_picked, "Name"):
                _pname = _picked.Name
                _like_val = int(girl.Girl_like.get(result, 500))

                if _like_val >= 750:
                    # Close friends
                    set_scene_expression(girl, "smile")
                    Say_Line(girl, _tl(_("Oh, %s! She's great. We're actually really close.")) % _pname)
                    Say_Line(girl, _("I'm glad you two are getting along. She's one of my favorite people here."))
                    Change_Status(girl, "Love", 3)
                elif _like_val >= 500:
                    # Friendly
                    set_scene_expression(girl, "smile")
                    Say_Line(girl, _tl(_("%s? Yeah, she's cool. We get along fine.")) % _pname)
                    Say_Line(girl, _("She's nice to hang around with. Good choice."))
                    Change_Status(girl, "Love", 2)
                elif _like_val >= 250:
                    # Distant
                    set_scene_expression(girl, "normal")
                    Say_Line(girl, _tl(_("%s, huh? I mean... we're not super close or anything.")) % _pname)
                    Say_Line(girl, _("She's fine, I guess. We just don't really click."))
                    Change_Status(girl, "Inbt", 2)
                else:
                    # Hostile
                    set_scene_expression(girl, "serious")
                    Say_Line(girl, _tl(_("%s? Seriously?")) % _pname)
                    Say_Line(girl, _("Let's just say... we don't exactly see eye to eye. Be careful around her."))
                    Change_Status(girl, "Inbt", 3)

        girl.set_flag("asked_talked_to_others", True)

    # ==========================================================
    # New simple/global college topics
    # ==========================================================

    def chitchat_global_coffee(girl, loc, t_index):
        _openers = [
            _("I think I'm running on coffee more than actual sleep this week."),
            _("Coffee is the only thing keeping me functional this semester."),
            _("I had three cups before noon. I think that's a record for me."),
        ]
        _followups = [
            _("If I fall asleep mid-sentence, just poke me or something."),
            _("At some point the caffeine stops working and you're just drinking warm sadness."),
            _("Want to grab one together later? Misery loves company."),
        ]
        set_scene_expression(girl, "sad")
        Say_Line(girl, _tl(renpy.random.choice(_openers)))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_followups)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_global_group_project(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Do you have a group for that project already?"))
        Say_Line(girl, _("Because half the campus is just pretending to 'work together' while one person does everything."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 1)

    def chitchat_global_cafeteria_food(girl, loc, t_index):
        _openers = [
            _("Have you tried the cafeteria food today?"),
            _("The cafeteria menu is getting more creative... and not in a good way."),
            _("I looked at my plate today and genuinely could not identify what I was eating."),
        ]
        _followups = [
            _("I'm not sure if it was lunch or a chemistry experiment."),
            _("We should start a petition for better food. Or just bring our own."),
            _("At least the bread is safe... most of the time."),
        ]
        set_scene_expression(girl, "disgusted")
        Say_Line(girl, _tl(renpy.random.choice(_openers)))
        set_scene_expression(girl, "sad")
        Say_Line(girl, _tl(renpy.random.choice(_followups)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_global_weekend_plans(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Any plans for the weekend?"))
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("I'm pretending I'll rest, but we both know I'll just scroll on my phone and panic Sunday night."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_phone_distraction(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        Say_Line(girl, _("I opened my phone to check one message and lost thirty minutes."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("If I ever go missing, I'm probably just trapped in social media again."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_global_late_to_class(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("I was almost late to class today."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("The worst part is, the teacher was even later than me."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 1)

    def chitchat_global_library(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("The library is either completely silent or full of chaos, there's no in-between."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("I kind of like both, depending on my mood."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 1)

    def chitchat_global_party_aftermath(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Did you hear about that party last night?"))
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("Some people showed up to class this morning looking like zombies with hangovers."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_sleep_deprived(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("How many hours of sleep did you get?"))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Be honest. Anything above five is considered a luxury here."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_global_campus_rumors(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Okay, don't repeat this, but people are saying two of the teachers are secretly dating."))
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("I have no proof. I just really want it to be true. Don't judge me."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_mr_johnson(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("You've talked to Mr. Johnson at his hot dog cart, right? He told me you 'sell much sausage'."))
        set_scene_expression(girl, "laugh")
        Say_Line(girl, _("I have been laughing about that all day. I don't even want to know what he means."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_weird_messages(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        Say_Line(girl, _("I keep getting these weird messages from someone with an unusual alias."))
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("I've already blocked like 3 numbers. Don't they have anything better to do?"))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_global_exam_week(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("Be honest, are you ready for exams? Because I am absolutely not."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("If we both fail, at least we fail together. That's kind of romantic, right?"))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_apocryphal_story(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Someone told me there's a secret room under the library that only staff can access."))
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Sounds totally apocryphal, but I kind of want to check anyway."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    # ---------- INTIMACY-GATED (reusable for multiple girls) ----------

    def chitchat_intimate_teasing(girl, loc, t_index):
        set_scene_expression(girl, "smile")

        if get_sex_count(girl, "bj") > 0:
            Say_Line(girl, _("It's hard to act normal after what we did the other night."))
            set_scene_expression(girl, "sly")
            Say_Line(girl, _("Try not to look too guilty when people are watching us."))
        elif get_sex_count(girl, "sex") > 0:
            Say_Line(girl, _("You expect me to talk about homework after we already slept together?"))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("You're bold. I kind of like that."))
        else:
            set_scene_expression(girl, "angry")
            Say_Line(girl, _("You like pushing things further every time we meet, don't you?"))
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("I'm keeping an eye on you."))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # ---------- FRIEREN ----------

    def chitchat_frieren_magic_books(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("There's a new magic theory book in the library."))
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Half the class will pretend to understand it."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_frieren_awkward_after_sex(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("About that night..."))
        set_scene_expression(girl, "angry")
        Say_Line(girl, _("No, forget it. Just... stay close."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 2)

    def chitchat_frieren_exam_logic(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Most exams don't really measure how smart you are."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("They just measure how well you can survive under pressure with limited sleep."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 1)

    # ---------- GWEN ----------

    def chitchat_gwen_training(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        Say_Line(girl, _("I should probably be training right now."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("But talking to you is a decent warm-up, I guess."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Obed", 1)

    def chitchat_gwen_sly_tease(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Remember when things got a bit handsy the other day?"))
        set_scene_expression(girl, "smirk")
        Say_Line(girl, _("Don't get too cocky. I can still pin you down in two seconds."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_gwen_gym_vs_study(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("If I spend one more hour sitting in class, my body might actually turn into a chair."))
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("I need the gym, or at least a long walk. Want to come next time?"))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Obed", 1)

    # ---------- POOL: SUNSCREEN ----------

    def _sunscreen_chitchat_ok(girl, loc, t_index):
        """Any girl at the pool in her bikini may ask. Not with her partner right there (she asks HIM), and not
        while she still flinches at your touch (GIRL_TOUCH_WARMUP: Rogue asks once her warm-up is over)."""
        return (loc == "pool" and getattr(girl, "_bikini_unlocked", False)
                and getattr(girl, "CurrentOutfitPreset", None) == "pool"
                and flirt_partner_watching(girl) is None
                and (_touch_warmup(girl, "shoulder_massage") or {}).get("left", 0) == 0)

    def chitchat_pool_sunscreen(girl, loc, t_index):
        """Pool-only topic: girl asks player to apply sunscreen on her back.
        Triggers the sunscreen loop (label _SunscreenLoop in Flirty.rpy)."""
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Hey, could you do me a favor? I can't reach my back with the sunscreen."))
        # The actual menu (accept/deny) is handled by the label
        renpy.call("_SunscreenStart", girl, loc, t_index)

    # ---------- STUDY READINESS ----------

    def chitchat_study_readiness(girl, loc, t_index):
        sl = getattr(girl, "study_level", 0)
        _dte = days_until_exam(store.Day) if hasattr(store, "Day") else 7
        _far = _dte > 5

        if sl >= 10:
            set_scene_expression(girl, "smile")
            _lines = [
                _("I feel really good about the next exam. {hint}I've been studying hard{/hint}."),

                _("I've put in the work. {hint}I'm confident I'll ace it{/hint}."),

                _("Honestly, {hint}I'm as ready as I'll ever be{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            if _far:
                _f = [
                    _("And we still have {hint}plenty of time{/hint}. I might even review again."),

                    _("With this much time left, {hint}I could help you study too{/hint}."),

                    _("No rush either. {hint}I've got this covered{/hint}."),

                ]
            else:
                _f = [
                    _("Good thing too, because {hint}the exam is almost here{/hint}."),

                    _("I could {hint}take it right now and be fine{/hint}."),

                    _("Bring it on. {hint}I'm ready{/hint}."),

                ]
            Say_Line(girl, _tl(renpy.random.choice(_f)))

        elif sl >= 7:
            set_scene_expression(girl, "smile")
            _lines = [
                _("{hint}I've been keeping up with my studies{/hint}. I think I'll do well."),

                _("I'm in a {hint}good place with studying{/hint}. Should be fine."),

                _("I've covered {hint}most of the material{/hint}. Feeling pretty confident."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            if _far:
                _f = [
                    _("And there's {hint}still time to polish up{/hint} the rest."),

                    _("I'll keep reviewing, but {hint}I'm not worried{/hint}."),

                    _("We have time. {hint}I'll be even more ready{/hint} by then."),

                ]
            else:
                _f = [
                    _("Not perfect, but {hint}I'm confident enough{/hint} for the test."),

                    _("A {hint}quick review{/hint} and I'll be all set."),

                    _("Just need to go over {hint}a few things{/hint} before the exam."),

                ]
            Say_Line(girl, _tl(renpy.random.choice(_f)))

        elif sl >= 5:
            set_scene_expression(girl, "normal")
            _lines = [
                _("{hint}I've studied a bit{/hint}. Should be enough to pass, I think."),

                _("I've done {hint}some reviewing{/hint}. Not a lot, but some."),

                _("I know {hint}the basics at least{/hint}. The rest... we'll see."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            if _far:
                set_scene_expression(girl, "normal")
                _f = [
                    _("But we {hint}still have time{/hint}, so I can catch up."),

                    _("I'm starting to look into it, but {hint}we still have time{/hint}."),

                    _("There's {hint}room to study more{/hint} before the exam."),

                ]
            else:
                set_scene_expression(girl, "sad")
                _f = [
                    _("But I wouldn't mind {hint}a few more study sessions{/hint} before the test..."),

                    _("I should probably {hint}cram a bit more{/hint} before the exam."),

                    _("The exam is close and {hint}I'm not fully ready{/hint}..."),

                ]
            Say_Line(girl, _tl(renpy.random.choice(_f)))

        elif sl >= 3:
            set_scene_expression(girl, "sad")
            _lines = [
                _("{hint}I haven't studied as much{/hint} as I should have..."),

                _("I've {hint}barely touched the material{/hint}, honestly."),

                _("My {hint}study game has been pretty weak{/hint} lately..."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            if _far:
                _f = [
                    _("But there's {hint}still time to catch up{/hint}. I hope."),

                    _("At least {hint}the exam isn't right away{/hint}. I need to start."),

                    _("I still have {hint}a window to study{/hint}. Better get on it."),

                ]
            else:
                _f = [
                    _("And the exam is soon... {hint}I might be in real trouble{/hint}."),

                    _("With the test coming up, {hint}I'm starting to panic{/hint}."),

                    _("I really {hint}need to cram{/hint}. The exam is almost here."),

                ]
            Say_Line(girl, _tl(renpy.random.choice(_f)))

        else:
            set_scene_expression(girl, "sad")
            _lines = [
                _("{hint}I haven't studied at all{/hint}... I'm going to fail for sure."),

                _("Study? {hint}I don't even know where my notes are{/hint}..."),

                _("I'm {hint}completely unprepared{/hint}. This is bad."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            if _far:
                set_scene_expression(girl, "normal")
                _f = [
                    _("At least there's {hint}still some time{/hint}... maybe I can start now."),

                    _("I should really get started. {hint}The exam isn't tomorrow{/hint} at least."),

                    _("Okay, I {hint}still have time{/hint}. No more excuses after today."),

                ]
            else:
                set_scene_expression(girl, "angry")
                _f = [
                    _("Please {hint}don't remind me about exams{/hint} right now."),

                    _("I don't want to think about it. {hint}I'm doomed{/hint}."),

                    _("At this point, {hint}I'm just hoping for a miracle{/hint}."),

                ]
            Say_Line(girl, _tl(renpy.random.choice(_f)))

        set_scene_expression(girl, "normal")
        girl.discover("discovered_study_level")
        Change_Status(girl, "Inbt", 1)

    # ---------- GIRL ASKS PLAYER ABOUT STUDYING ----------

    def chitchat_girl_asks_player_study(girl, loc, t_index):
        _ask_lines = [
            _("By the way... have you been studying?"),
            _("So... how's the studying going on your end?"),
            _("Be honest with me. Have you been reviewing the material?"),
        ]
        set_scene_expression(girl, "normal")
        Say_Line(girl, _tl(renpy.random.choice(_ask_lines)))

        psl = getattr(store.Player, "study_level", 0) if hasattr(store, "Player") else 0
        _dte = days_until_exam(store.Day) if hasattr(store, "Day") else 7
        _far = _dte > 5

        if psl >= 10:
            _p = [
                _("Yeah, I've been hitting the books hard. I'm ready for anything."),
                _("I've studied more than enough. Bring on the exam."),
                _("Honestly, I feel great about it. I've been really focused."),
            ]
            Say_Player(_tl(renpy.random.choice(_p)))
            set_scene_expression(girl, "smile")
            _g = [
                _("Wow, look at you being responsible. I'm impressed."),
                _("That's great! Wish I had that discipline."),
                _("Nice. Guess I don't have to worry about you then."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_g)))

        elif psl >= 7:
            _p = [
                _("I've been studying a decent amount. Should be fine."),
                _("Yeah, I've covered most of the material. Feeling okay about it."),
                _("I've been putting in some hours. Not perfect, but solid."),
            ]
            Say_Player(_tl(renpy.random.choice(_p)))
            set_scene_expression(girl, "smile")
            _g = [
                _("Good. At least one of us has it together."),
                _("That's reassuring. Keep it up."),
                _("Sounds like you're on track. Good for you."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_g)))

        elif psl >= 5:
            _p = [
                _("A bit here and there. Nothing crazy."),
                _("I've done some reviewing. Enough to not be lost, I think."),
                _("I've looked over the basics at least."),
            ]
            Say_Player(_tl(renpy.random.choice(_p)))
            set_scene_expression(girl, "normal")
            if _far:
                _g = [
                    _("Well, you still have time to improve. Don't waste it."),
                    _("I'm starting to look into it too, but we still have time."),
                    _("At least you have a head start. Keep going."),
                ]
            else:
                _g = [
                    _("Hmm... you might want to step it up a little. The exam is close."),
                    _("That might not be enough with the test coming up soon..."),
                    _("Better cram a bit more. We're running out of time."),
                ]
            Say_Line(girl, _tl(renpy.random.choice(_g)))

        elif psl >= 3:
            _p = [
                _("Honestly? Not much."),
                _("I've barely opened the textbook..."),
                _("Study? Define 'study'... because I haven't done much."),
            ]
            Say_Player(_tl(renpy.random.choice(_p)))
            set_scene_expression(girl, "sad")
            if _far:
                _g = [
                    _("Well... at least there's still time. You should get on it."),
                    _("That's not great, but the exam isn't tomorrow. Start now."),
                    _("You've got a window. Don't let it close without studying."),
                ]
            else:
                _g = [
                    _("That's not great... the exam is almost here."),
                    _("You might be in trouble. The test is coming up fast."),
                    _("Maybe we should study together. You need the help."),
                ]
            Say_Line(girl, _tl(renpy.random.choice(_g)))

        else:
            _p = [
                _("Study? I've been... busy with other things."),
                _("What's studying? Never heard of it."),
                _("I haven't touched a single page. Don't look at me like that."),
            ]
            Say_Player(_tl(renpy.random.choice(_p)))
            set_scene_expression(girl, "angry")
            if _far:
                _g = [
                    _("You still have time, but you really need to start. Seriously."),
                    _("At least the exam isn't right away. Please start studying."),
                    _("Don't push it. You need to start before it's too late."),
                ]
            else:
                _g = [
                    _("You're going to regret that when the exam comes. Trust me."),
                    _("The exam is practically here and you haven't studied at all?!"),
                    _("I can't help you if you don't help yourself. Get to it!"),
                ]
            Say_Line(girl, _tl(renpy.random.choice(_g)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Inbt", 1)

    # ---------- ASK PLAYER'S FAVORITE POSITION ----------

    def chitchat_ask_player_fav(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("So... I've been curious. What's your favorite thing to do with a girl?"))

        _POSE_FOR_FAV = {"tj": "titjob", "cowgirl": "cowgirl", "reverse_cowgirl": "reverse_cowgirl", "laying_down": "laying_down"}
        _all_choices = [
            (_("Handjob"), "hj"),
            (_("Blowjob"), "bj"),
            (_("Titjob"), "tj"),
            (_("Riding"), "cowgirl"),
            (_("Reverse Cowgirl"), "reverse_cowgirl"),
            (_("Laying Down"), "laying_down"),
        ]
        choices = [(lbl, val) for lbl, val in _all_choices if girl_has_pose(girl, _POSE_FOR_FAV.get(val, val))]
        result = renpy.display_menu(choices)

        girl.player_fav_position = result

        if result == "tj" and not girl_has_pose(girl, "titjob"):
            set_scene_expression(girl, "sad", eyes="eyes_side")
            Say_Line(girl, renpy.random.choice([
                _("You... want that? With me?"),
                _("I... don't think I can give you that."),
                _("Oh. That's... not really something I can do."),
            ]))
            Change_Status(girl, "Love", -3)
        else:
            _FAV_REACTIONS = {
                "hj": _("Hands, huh? Simple but effective. I can respect that."),
                "bj": _("Oh... good to know. I'll keep that in mind."),
                "tj": _("Really? You like that? Interesting..."),
                "cowgirl": _("A guy who likes the girl on top... I like that."),
                "reverse_cowgirl": _("From behind, huh? Bold choice. Noted."),
                "laying_down": _("You like being on top and in control? Noted."),
            }
            Say_Line(girl, _FAV_REACTIONS.get(result, "Interesting..."))
            Change_Status(girl, "Love", 2)
            Change_Status(girl, "Inbt", 3)

        set_scene_expression(girl, "normal")

    # ---------- GYM TOPICS ----------

    def chitchat_global_gym_soreness(girl, loc, t_index):
        _open = [
            _("I'm so sore from yesterday's workout..."),
            _("My legs are killing me after the gym."),
            _("I can barely move today. The gym destroyed me."),
        ]
        set_scene_expression(girl, "sad")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("But I guess that means it's working, right?"),
            _("Pain is just progress in disguise... or so they say."),
            _("At least I know I actually did something for once."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Obed", 1)

    def chitchat_global_gym_motivation(girl, loc, t_index):
        _open = [
            _("Have you been hitting the gym lately?"),
            _("I've been trying to go to the gym more often."),
            _("I need to get back into a workout routine."),
        ]
        set_scene_expression(girl, "normal")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("We should go together sometime. It's more fun that way."),
            _("Having a gym buddy makes it way easier to stay consistent."),
            _("Maybe if we go together, I'll actually stick to it."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Obed", 2)
        Change_Status(girl, "Love", 1)

    def chitchat_global_gym_crowded(girl, loc, t_index):
        _open = [
            _("The gym was so packed today, I could barely find a spot."),
            _("I went to the gym earlier and there was a line for every machine."),
            _("Everyone decided to work out at the same time today..."),
        ]
        set_scene_expression(girl, "angry")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("Next time I'm going super early. No one else will be awake."),
            _("I spent more time waiting than actually lifting."),
            _("Maybe I should just do push-ups in my room instead."),
        ]
        set_scene_expression(girl, "sad")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Obed", 1)

    # ---------- EXAM / A GRADE TOPICS ----------

    def chitchat_global_exam_help(girl, loc, t_index):
        _open = [
            _("So... you actually got an A on that exam?"),
            _("I heard you aced the last exam. That's impressive."),
            _("Wait, you got an A? Seriously?"),
        ]
        set_scene_expression(girl, "surprise")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("Think you could help me study for the next one? I could really use it."),
            _("Can you tutor me before the next exam? I'll bring snacks."),
            _("You have to help me study. I'm not surviving the next one alone."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_exam_together(girl, loc, t_index):
        _open = [
            _("You did so well on that exam... meanwhile I barely passed."),
            _("I wish I had your study habits. That A was no joke."),
            _("Okay, I need your secret. How did you get an A?"),
        ]
        set_scene_expression(girl, "sad")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("We should study together next time. Maybe some of your brains will rub off on me."),
            _("Let's be study partners. You clearly know what you're doing."),
            _("How about we hit the library together before the next test?"),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Obed", 1)

    # ---------- MAX ENERGY / FITNESS TOPICS ----------

    def chitchat_global_max_energy(girl, loc, t_index):
        _open = [
            _("Okay, have you been working out more? You look... different."),
            _("I don't wanna be weird, but you've gotten way more fit lately."),
            _("You've been hitting the gym hard, huh? I can tell."),
        ]
        set_scene_expression(girl, "surprise")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("We should train together sometime. You can show me some exercises."),
            _("Think you could teach me your routine? I need a gym buddy."),
            _("Let's work out together. I bet you could push me to actually try."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Obed", 1)

    # ---------- POOL TOPICS ----------

    def chitchat_global_pool_relaxing(girl, loc, t_index):
        _open = [
            _("The pool was so nice today. Super relaxing."),
            _("I spent some time at the pool earlier. The water was perfect."),
            _("There's nothing like a good swim to clear your head."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("We should go together next time. It'd be fun."),
            _("I could spend hours there if I didn't have things to do."),
            _("Honestly, it's the best part of this campus."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_global_pool_tan(girl, loc, t_index):
        _open = [
            _("I was thinking about laying out by the pool later."),
            _("The sun has been great for tanning by the pool."),
            _("Have you noticed how nice the weather is? Perfect pool day."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("I need to even out my tan lines... don't look at me like that."),
            _("A little sun does wonders. You should try it."),
            _("Maybe I'll actually swim this time instead of just lying there."),
        ]
        set_scene_expression(girl, "normal")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Inbt", 1)

    def chitchat_global_pool_splash(girl, loc, t_index):
        _open = [
            _("Someone splashed me at the pool today. On purpose."),
            _("I was just relaxing by the pool and someone cannonballed right next to me."),
            _("The pool was chaos today. People were splashing everywhere."),
        ]
        set_scene_expression(girl, "angry")
        Say_Line(girl, _tl(renpy.random.choice(_open)))

        _follow = [
            _("I got my revenge though. They didn't see it coming."),
            _("My hair was completely ruined. I'm still annoyed."),
            _("Next time I'm bringing a water gun for payback."),
        ]
        set_scene_expression(girl, "smile")
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    # ---------- SHOWER HISTORY ----------

    def chitchat_girl_caught_player_shower(girl, loc, t_index):
        """Girl references walking in on the player showering.  +Inbt"""
        _best = max(getattr(girl, "Love", 0), getattr(girl, "Inbt", 0))

        if _best >= 500:
            _open = [
                _("You know... I still think about walking in on you in the shower."),
                _("Remember when I walked in on you? That image is stuck in my head."),
                _("I keep replaying that shower moment in my mind..."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("Maybe next time I won't leave so quickly."),
                _("I wouldn't mind a repeat, honestly."),
                _("You didn't seem to mind either, did you?"),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
        elif _best >= 250:
            _open = [
                _("About that time I walked in on you in the shower..."),
                _("So... the shower thing. Can we talk about that?"),
                _("I still feel weird about walking in on you like that."),
            ]
            set_scene_expression(girl, "normal")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("I didn't mean to see... everything. But I did."),
                _("Sorry about that. Well... mostly sorry."),
                _("Let's just pretend it didn't happen. Or not. Up to you."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
        else:
            _open = [
                _("I'm still embarrassed about walking in on you..."),
                _("Can we please never talk about the shower thing?"),
                _("I still can't look at you without thinking about that shower incident."),
            ]
            set_scene_expression(girl, "embarrassed")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("I swear I didn't know you were in there!"),
                _("I knocked! ...Okay, maybe I didn't knock hard enough."),
                _("Next time I'm checking twice before opening any door."),
            ]
            set_scene_expression(girl, "angry")
            Say_Line(girl, _tl(renpy.random.choice(_follow)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_girl_comments_player_size(girl, loc, t_index):
        """Girl comments on the player's size after seeing him nude."""
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

        if _has_bf:
            # She starts comparing to boyfriend but stops mid-sentence
            set_scene_expression(girl, "embarrassed")
            _lines = [
                _("You know... compared to my %(pl)s, you're... um..."),
                _("I wasn't going to say anything but... you're bigger than... never mind."),
                _("My %(pl)s is... well, let's just say you're... I shouldn't say this."),
                _("I keep thinking about... you're definitely more... forget I said anything."),
            ]
            Say_Line(girl, _format_partner_line(girl, renpy.random.choice(_lines)))
            set_scene_expression(girl, "normal")
            _follow = [
                _("Forget I said anything! I didn't mean to compare..."),
                _("Don't look at me like that! I just... noticed, okay?"),
                _("Oh god, I said that out loud, didn't I? Just forget it."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Obed", 3)
        else:
            set_scene_expression(girl, "shy")
            _lines = [
                _("So... I've been meaning to say... you're pretty well endowed."),
                _("I can't stop thinking about... you know. What I saw. You're impressive."),
                _("Don't let this go to your head, but... you're bigger than I expected."),
                _("I had a dream about... well, about what I saw. You're... yeah."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            set_scene_expression(girl, "normal")
            _follow = [
                _("Sorry, that was forward. But I had to say it."),
                _("Just being honest. A girl notices these things."),
                _("Anyway! Moving on. Totally normal conversation."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Obed", 2)

    def chitchat_player_caught_girl_shower(girl, loc, t_index):
        """Girl references the player walking in on her in the shower area."""
        _best = max(getattr(girl, "Love", 0), getattr(girl, "Inbt", 0))

        if _best >= 500:
            _open = [
                _("You know, when you walked in on me that time... I didn't really mind."),
                _("Remember when you caught me in the shower? I think about it sometimes."),
                _("That time you walked in on me... I wasn't as upset as I pretended to be."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("Maybe I left the door unlocked on purpose. Who knows?"),
                _("You liked what you saw, didn't you? Don't lie."),
                _("Next time, maybe just... stay a little longer."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
        elif _best >= 250:
            _open = [
                _("About that time you walked in on me..."),
                _("So, we're just going to pretend you didn't see me like that?"),
                _("You really need to learn how to knock, you know."),
            ]
            set_scene_expression(girl, "normal")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("I'm not mad. Just... surprised you didn't look away faster."),
                _("At least tell me you enjoyed the view. Otherwise it's just awkward."),
                _("I guess it's only fair since... well, never mind."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
        else:
            _open = [
                _("You barging in while I was showering... that was NOT okay."),
                _("I'm still upset you saw me like that without warning."),
                _("Do you just open every door without knocking?!"),
            ]
            set_scene_expression(girl, "angry")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("Next time, I'm locking the door. Twice."),
                _("You owe me an apology. A real one."),
                _("If it happens again, I'm throwing something at you."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_follow)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_showered_together(girl, loc, t_index):
        """Girl references having showered together with the player."""
        _best = max(getattr(girl, "Love", 0), getattr(girl, "Inbt", 0))

        if _best >= 500:
            _open = [
                _("Showering together was... really nice, actually."),
                _("I keep thinking about our shower together. In a good way."),
                _("That shower we shared? Highlight of my week."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("We should make that a regular thing."),
                _("I wouldn't say no if you asked again."),
                _("The hot water wasn't the only thing making me warm in there."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_follow)))
        else:
            _open = [
                _("That shower together was... interesting."),
                _("So we showered together. That happened."),
                _("I'm still processing the whole showering together thing."),
            ]
            set_scene_expression(girl, "normal")
            Say_Line(girl, _tl(renpy.random.choice(_open)))
            _follow = [
                _("It wasn't bad. Just... unexpected."),
                _("Don't go telling anyone about that, okay?"),
                _("I'm not saying I hated it. I'm just saying... don't assume."),
            ]
            set_scene_expression(girl, "smile")
            Say_Line(girl, _tl(renpy.random.choice(_follow)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)
        Change_Status(girl, "Love", 2)

    # ---------- HIGH LUST COMMENTARY ----------

    def chitchat_high_lust(girl, loc, t_index):
        orgasms = getattr(girl, "Orgasms", {})
        fav = getattr(girl, "FavoriteAct", None)
        player_fav = getattr(girl, "player_fav_position", None)

        set_scene_expression(girl, "smile")

        # Try to reference an act she's done before
        _lust_lines_by_act = {
            "hj": [
                _("I keep thinking about wrapping my hand around it again..."),
                _("My hands feel restless today... wonder why."),
                _("I wouldn't mind giving you another handjob right now."),
            ],
            "bj": [
                _("I can't stop thinking about having it in my mouth..."),
                _("I've been thinking about going down on you again..."),
                _("My lips feel lonely... if you know what I mean."),
            ],
            "tj": [
                _("My chest feels warm today... I wonder why."),
                _("I keep thinking about last time you were between my breasts..."),
                _("I wouldn't mind feeling you between them again."),
            ],
            "cowgirl": [
                _("I really feel like riding something right now..."),
                _("I want to be on top again... is that too forward?"),
                _("I can't stop thinking about riding you."),
            ],
            "reverse_cowgirl": [
                _("I keep thinking about you behind me..."),
                _("I want to feel you from behind again..."),
                _("On all fours sounds really good right now..."),
            ],
            "masturbate": [
                _("I've been... touching myself thinking about you."),
                _("I could really use some alone time right now... or not alone."),
                _("I've been feeling restless... in a good way."),
            ],
        }

        # Pick from acts she's actually done, prioritizing her favorite or the player's
        done_acts = [act for act in _lust_lines_by_act if orgasms.get(act, 0) > 0]

        pick = None
        if player_fav and player_fav in done_acts:
            pick = player_fav
        elif fav and fav in done_acts:
            pick = fav
        elif done_acts:
            pick = renpy.random.choice(done_acts)

        if pick:
            line = renpy.random.choice(_lust_lines_by_act[pick])
            Say_Line(girl, line)
        else:
            # No acts done yet, generic lust line
            _generic_lust = [
                _("I've been feeling... distracted today. In a good way."),
                _("Is it hot in here or is it just me?"),
                _("I can't focus on anything today... my mind keeps wandering."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_generic_lust)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # ---------- TRAIT-HINT TOPICS (global) ----------

    def chitchat_hint_cameras(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Have you seen how many people are glued to their phones filming everything?"))

        if girl.has_trait("camera_lover"):
            set_scene_expression(girl, "smile")
            _lines = [
                _("Honestly, I get it. {hint}I love taking selfies{/hint}. My gallery is insane."),

                _("{hint}I record everything{/hint}. Memories deserve to be saved, right?"),

                _("I'm totally that person. {hint}My camera roll is my diary{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_camera_lover")
        elif girl.has_trait("camera_hater"):
            set_scene_expression(girl, "angry")
            _lines = [
                _("It drives me crazy. Everyone filming all the time, {hint}no privacy left{/hint}."),

                _("{hint}I hate being tagged in photos{/hint}. Just let me exist in peace."),

                _("If someone {hint}points a camera at me, I lose it{/hint}. Seriously."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_camera_hater")
        else:
            set_scene_expression(girl, "normal")
            _lines = [
                _("I don't really care either way. Some people go overboard, though."),
                _("I take a photo now and then, but I'm not obsessed with it."),
                _("Phone culture is weird, but I don't have strong feelings about it."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_hint_protection(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("A friend told me about a pregnancy scare she had recently..."))

        if girl.has_trait("cum_slut"):
            set_scene_expression(girl, "smile")
            _lines = [
                _("Honestly, {hint}I'd rather feel everything{/hint}. The risk is part of the thrill."),

                _("She's overreacting. {hint}Some things are worth the risk{/hint}."),

            ]
            # "I never bother": a habit, so only once she is past discovering it AND has gone raw
            if trait_is_veteran(girl, "cum_slut") and getattr(girl, "raw_sex_count", 0) > 0:
                _lines.append(_("I mean... {hint}protection kills the vibe{/hint}, doesn't it? I never bother."))
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_cum_slut")
        elif girl.has_trait("hate_cum"):
            set_scene_expression(girl, "angry")
            _lines = [
                _("That's exactly why {hint}you always use protection. No exceptions{/hint}."),

                _("{hint}I always carry my own{/hint}. I don't trust anyone else to be careful."),

                _("Carelessness like that {hint}disgusts me{/hint}. It's not that hard to be safe."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_hate_cum")
        else:
            set_scene_expression(girl, "normal")
            _lines = [
                _("It's just common sense, right? Be smart about it and you're fine."),
                _("I feel bad for her, but that's why you plan ahead."),
                _("Scary situation. I try not to overthink it, but I'm careful."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_hint_public_thrill(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Someone dared a guy to streak across campus yesterday. Can you believe it?"))

        if girl.has_trait("public_fetish"):
            set_scene_expression(girl, "smile")
            _lines = [
                _("The thrill of {hint}almost being caught{/hint}... I totally get it."),

                _("I won't lie, the idea of {hint}doing something risky in public excites me{/hint}."),

                _("I've had my own moments. {hint}Not streaking, but... close enough{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_public_fetish")
        elif girl.has_trait("public_shy"):
            set_scene_expression(girl, "worried")
            _lines = [
                _("{hint}I'd die if that were me{/hint}. Just thinking about it makes me anxious."),

                _("How could anyone do that? {hint}I'd never risk being seen{/hint} like that."),

                _("That's terrifying. {hint}I need privacy for... everything{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_public_shy")
        else:
            set_scene_expression(girl, "normal")
            _lines = [
                _("It's kind of funny, but I wouldn't do it myself. Maybe something milder."),
                _("I'm open to a little adventure, but that's extreme."),
                _("I'd need to feel really safe before trying anything risky like that."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_hint_intensity(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("So... I've been thinking about what I really crave lately."))

        if girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, "smile")
            _lines = [
                _("I want intensity. {hint}I want to be thrown around{/hint}. Is that too much?"),

                _("Gentle is fine for some people, but {hint}I need more. Way more{/hint}."),

                _("{hint}I want to feel it the next day{/hint}. That's how I know it was good."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            set_scene_expression(girl, "shy")
            _lines = [
                _("{hint}I want tenderness{/hint}. Slow dancing before bed, eye contact during..."),

                _("{hint}Gentle and close{/hint}. That's what makes me feel something real."),

                _("I don't need fireworks. Just {hint}hold me like you mean it{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_cute_sex")
        else:
            set_scene_expression(girl, "normal")
            _lines = [
                _("Honestly? It depends on my mood. I don't have one specific thing."),
                _("Sometimes soft, sometimes intense. I like variety."),
                _("I haven't figured it out yet. Both sound good to me."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # ==========================================================
    # ANAL PREFERENCE CHITCHATS
    # ==========================================================

    def chitchat_hint_anal(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("A friend of mine mentioned trying... you know... the other way. With her boyfriend."))

        if girl.has_trait("anal_lover"):
            set_scene_expression(girl, "smile")
            _lines = [
                _("Honestly? {hint}I get it. I think about it a lot{/hint}. Is that weird?"),

                _("{hint}The idea of it really excites me{/hint}. Like... a lot."),

                _("She said she loved it and {hint}I can totally see why{/hint}. Some things just hit different."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_anal_lover")
        elif girl.has_trait("anal_hater"):
            set_scene_expression(girl, "worried")
            _lines = [
                _("{hint}That sounds awful{/hint}. Why would anyone want that?"),

                _("I could NEVER. {hint}Just thinking about it makes me uncomfortable{/hint}."),

                _("She's braver than me. {hint}I'd rather do literally anything else{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_anal_hater")
        else:
            set_scene_expression(girl, "normal")
            _lines = [
                _("I don't know how I'd feel about it. Curious, I guess, but also nervous."),
                _("I mean... I'd have to really trust someone before trying something like that."),
                _("It's not something I think about much, honestly. But I wouldn't rule it out."),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    def chitchat_anal_reflection(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("So... about last time. The, uh... anal thing."))

        if girl.has_trait("anal_lover") and trait_is_discovering(girl, "anal_lover"):
            # still discovering it: surprised by how much she liked it, no "my favorite" yet
            set_scene_expression(girl, "embarrassed")
            _lines = [
                _("I can't stop thinking about it. {hint}When can we do that again?{/hint}"),

                _("I didn't think I'd like it that much... {hint}I really did{/hint}. Is that weird?"),

                _("It was so much better than I expected. {hint}I think I want to do it again{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_anal_lover")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("anal_lover"):
            set_scene_expression(girl, "smile")
            _lines = [
                _("I can't stop thinking about it. {hint}When can we do that again?{/hint}"),

                _("My ass still remembers you. {hint}In the best way possible{/hint}~"),

                _("That was incredible. {hint}Anal is definitely my favorite{/hint}. Just so you know."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_anal_lover")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("anal_hater"):
            set_scene_expression(girl, "angry")
            _lines = [
                _("{hint}I hated every second of it{/hint}. My ass hurt for DAYS."),

                _("I still can't sit properly. {hint}Please don't ever ask me to do that again{/hint}."),

                _("That was genuinely awful. {hint}I don't understand how anyone enjoys that{/hint}."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_trait_anal_hater")
            Change_Status(girl, "Love", -2)
        else:
            _lines = [
                _("It was... different. I'm still processing how I feel about it honestly."),
                _("I didn't hate it, but I didn't love it either. Maybe with more practice?"),
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        set_scene_expression(girl, "normal")

    def chitchat_anal_hater_confrontation(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        _sa = getattr(girl, "Sex_acts", {}) or {}
        _anal_count = _sa.get("anal", 0)

        if _anal_count >= 2:
            Say_Line(girl, _("We need to talk. You keep putting it in my ass and I HATE it."))
            _lines = [
                _("Every single time it hurts. Do you even care? {hint}I dread it{/hint}."),

                _("My ass is not a toy. {hint}I genuinely suffer when you do that{/hint}. You know that, right?"),

                _("How many times do I have to tell you? {hint}I hate anal{/hint}. I'm starting to wonder if you even listen."),

            ]
        else:
            Say_Line(girl, _("About what you did to my ass..."))
            _lines = [
                _("{hint}It was awful{/hint}. I'm not going to pretend otherwise."),

                _("I trusted you and you did the one thing {hint}I hate the most{/hint}."),

                _("My ass still hurts. {hint}I hope you're happy{/hint}."),

            ]

        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "sad")
        Say_Line(girl, _("Just... think about how I feel next time. Please."))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", -3)
        Change_Status(girl, "Obed", 2)

    # ==========================================================
    # DISCOVERY CHITCHATS (replace direct questions)
    # ==========================================================

    # --- Boyfriend discovery ---
    def chitchat_discover_boyfriend(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        _opener = [
            _("A friend of mine just broke up with her boyfriend. Drama everywhere."),
            _("Someone asked me if I was single today. Out of nowhere."),
            _("Couples on campus are so annoying sometimes, don't you think?"),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_opener)))

        _has_bf = _is_bf_context(girl)
        _is_ch = _is_cheater(girl)

        if _has_bf and _is_ch:
            set_scene_expression(girl, "smile")
            _pl = girl.partner_label()
            _lines = [
                _tl(_("{hint}I have a %s{/hint}... technically. But honestly, {hint}it's complicated{/hint}.")) % _pl,
                _("Yeah, {hint}I'm with someone{/hint}. Not that it matters much to me."),

                _tl(_("I do have a {hint}%s{/hint}. But let's just say {hint}I keep my options open{/hint}.")) % _pl,
            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            _discover_partner(girl)
            girl.discover("discovered_relationship")
        elif _has_bf:
            set_scene_expression(girl, "normal")
            _pl = girl.partner_label()
            _t = int(girl.Temptation)
            if _t <= 2:
                _lines = [
                    _format_partner_line(girl, _("Speaking of which... {hint}I do have a %(pl)s{/hint}. %(Pp)s's really sweet.")),
                    _("Relationships are tricky. {hint}Mine is going well{/hint}, though."),

                    _format_partner_line(girl, _("{hint}I'm taken{/hint}, actually. %(Pp)s's a good one.")),
                ]
            elif _t <= 5:
                _lines = [
                    _tl(_("I... yeah, {hint}I have a %s{/hint}. Things are... fine, I guess.")) % _pl,
                    _("{hint}I'm with someone{/hint}. Not sure why I hesitated saying that."),

                    _tl(_("I do have a {hint}%s{/hint}. Lately, though... it's been weird.")) % _pl,
                ]
            else:
                _lines = [
                    _tl(_("I technically have a {hint}%s{/hint}. But {hint}I don't know anymore{/hint}...")) % _pl,
                    _("{hint}I'm with someone{/hint}. Or at least, I think I am. {hint}It's complicated{/hint}."),

                    _tl(_("Yeah, I have a {hint}%s{/hint}. But {hint}things haven't been great{/hint} between us.")) % _pl,
                ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            _discover_partner(girl)
            girl.discover("discovered_relationship")
        else:
            set_scene_expression(girl, "smile")
            _lines = [
                _("Me? {hint}I'm single{/hint}, actually. Haven't found anyone worth my time yet."),

                _("{hint}I'm not seeing anyone{/hint}. I'm enjoying my freedom for now."),

                _("{hint}I'm not with anyone{/hint} right now. Why, are you volunteering?"),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
            girl.discover("discovered_single")
            girl.discover("discovered_relationship")

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    # --- Virginity discovery ---
    def chitchat_discover_virgin(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        _opener = [
            _("I overheard some girls talking about their first time today..."),
            _("Someone in class made a joke about being 'experienced.' So awkward."),
            _("There's so much pressure about... you know, your first time."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_opener)))

        if girl.has_trait("virgin"):
            set_scene_expression(girl, "shy")
            _lines = [
                _("I... {hint}haven't actually done it yet{/hint}. Is that weird?"),

                _("Honestly? {hint}I'm still waiting{/hint}. I want it to be with the right person."),

                _("{hint}I haven't been with anyone{/hint} like that. I'm not in a rush."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))
        else:
            set_scene_expression(girl, "smile")
            _lines = [
                _("I'm {hint}not exactly inexperienced{/hint}, if that's what you're wondering."),

                _("Let's just say {hint}I've had my share{/hint} of... experiences."),

                _("{hint}I've been with someone{/hint} before. It was... a thing."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_lines)))

        girl.discover("discovered_virgin")
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

        # Other girls present overhear virginity status
        if girl.has_trait("virgin"):
            _loc = getattr(store, "CurrentLocation", None)
            if _loc:
                for _og in ALL_GIRLS:
                    if _og.gid != girl.gid and _og.loc == _loc:
                        girl_learns_virgin(_og, girl)

    # --- Favorite act discovery ---
    def chitchat_discover_fav_act(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _opener = [
            _("You know what I was thinking about the other day?"),
            _("Can I tell you something kind of personal?"),
            _("I've been in a weird mood lately... thinking about things."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_opener)))

        _fav = getattr(girl, "FavoriteAct", None)
        _flags = getattr(girl, "intimacy_flags", set()) or set()

        # If her favorite act isn't something she's actually done, pick one she has
        if _fav and _fav not in _flags:
            _done_acts = [a for a in _flags if a in ("kiss", "massage", "hj", "bj", "tj", "reverse_cowgirl", "cowgirl", "doggy", "full_nelson", "laying_down", "masturbate")]
            if _done_acts:
                _fav = _tl(renpy.random.choice(_done_acts))
            else:
                # She hasn't done anything yet — generic deflection
                Say_Line(girl, _("I haven't really figured out what I like yet. Maybe you can help me find out?"))
                set_scene_expression(girl, "normal")
                return

        _FAV_LINES = {
            "kiss": [
                _("There's nothing better than {hint}a really good kiss{/hint}. It just hits different."),

                _("{hint}Kissing{/hint} is so underrated. A good kiss can change everything."),

                _("I'm a sucker for {hint}kissing{/hint}. That's my thing, honestly."),

            ],
            "massage": [
                _("A good {hint}massage{/hint}... that's all I need to be happy."),

                _("I could melt under someone's hands. {hint}Massages{/hint} are everything."),

                _("I swear, a {hint}massage{/hint} is better than most things in life."),

            ],
            "hj": [
                _("I like being in control {hint}with my hands{/hint}. There's something satisfying about it."),

                _("I enjoy the {hint}hands-on approach{/hint}. There's a certain power in it."),

                _("{hint}Working with my hands{/hint}... I'm surprisingly good at it."),

            ],
            "bj": [
                _("I kind of like... {hint}using my mouth{/hint}. Don't make it weird."),

                _("Let's just say {hint}I'm an oral person{/hint}. I'll leave it at that."),

                _("There's something about {hint}going down{/hint} that I really enjoy."),

            ],
            "tj": [
                _("I like using {hint}what I've got up here{/hint}. It's fun, honestly."),

                _("{hint}These aren't just for show{/hint}, you know."),

                _("I enjoy putting {hint}my chest{/hint} to good use. Don't judge."),

            ],
            "reverse_cowgirl": [
                _("I like it {hint}from behind{/hint}. Something about it just hits different."),

                _("Being taken {hint}from behind{/hint}... it's my thing. End of story."),

                _("There's something primal about it. {hint}From behind{/hint}, I mean."),

            ],
            "cowgirl": [
                _("I like {hint}being on top{/hint}. The control, the view... everything."),

                _("Being in charge {hint}on top{/hint}... nothing beats that feeling."),

                _("I prefer {hint}setting the pace myself{/hint}. On top, obviously."),

            ],
            "masturbate": [
                _("Sometimes I just like {hint}taking care of myself{/hint}. It's personal."),

                _("I enjoy {hint}my own company{/hint}, if you know what I mean."),

                _("A girl has needs. Sometimes {hint}I handle them on my own{/hint}."),

            ],
        }
        _lines = _FAV_LINES.get(_fav, [_("I haven't really figured that out yet.")])
        Say_Line(girl, _tl(renpy.random.choice(_lines)))

        girl.discover("discovered_fav_act")
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # --- Favorite drink HINT (tier only) ---
    # This is only a hint: she says whether she likes something strong/medium/
    # weak. It does NOT reveal the preference for certain — that only happens
    # during an event (serving her the drink). No discover() call here.
    def chitchat_hint_fav_drink(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _openers = [
            _("Ugh, you know what I could really go for right now?"),
            _("Can I be honest about what I'm craving?"),
            _("Long day... it's got me thinking about how I like to unwind."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_openers)))

        # FavoriteDrink is a generic tier key ("low"/"med"/"high"); lines
        # reference the type, never the brand (which differs per language).
        _tier = getattr(girl, "FavoriteDrink", None)
        if _tier not in DRINK_PREF_LINES:
            _tier = "low"
        Say_Line(girl, _tl(renpy.random.choice(DRINK_PREF_LINES[_tier])))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    # --- Favorite food HINT (dish type / dieting) ---
    # Same rule: a hint only. She talks about the kind of food she likes (or
    # that she's eating light). Certainty comes from the restaurant event.
    _FAV_FOOD_HINT_LINES = {
        "steak": [
            _("Honestly? Nothing beats a good steak. I'm a total carnivore."),
            _("Give me a juicy steak and I'm a happy girl. Red meat is my weakness."),
        ],
        "pasta": [
            _("Pasta is my ultimate comfort food. I could honestly eat it every day."),
            _("Carbs are life. A big bowl of pasta fixes any bad day for me."),
        ],
        "chicken": [
            _("I could eat chicken a hundred different ways and never get bored."),
            _("Grilled chicken is my safe order anywhere. Simple, but I love it."),
        ],
        "salad": [
            _("I try to keep it light lately... lots of salads and fresh stuff."),
            _("I'm kind of watching what I eat, so salad is usually my go-to."),
        ],
    }

    def chitchat_hint_fav_food(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _openers = [
            _("Random, but I've been thinking about food all day."),
            _("Okay, don't judge me, but can we talk about food for a second?"),
            _("I get way too excited about what I'm going to eat later."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_openers)))

        _dish = getattr(girl, "FavoriteDish", None)
        if _dish not in _FAV_FOOD_HINT_LINES:
            _dish = "pasta"
        Say_Line(girl, _tl(renpy.random.choice(_FAV_FOOD_HINT_LINES[_dish])))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    # ==========================================================
    # HISTORY-BASED CHITCHAT (trait-aware)
    # ==========================================================

    # --- After first sex (penetration) ---
    def chitchat_history_first_sex(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        if girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("I still think about our first time together... {hint}it felt special{/hint}."),

                _("{hint}You were gentle with me{/hint}. I appreciate that more than you know."),

                _("Every time I see you, I remember {hint}how nervous I was{/hint} that night."),

            ]))
            girl.discover("discovered_trait_cute_sex")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("You know, our first time was good... but {hint}I want it rougher{/hint} next time."),

                _("I've been craving {hint}something more intense{/hint} since we did it."),

                _("{hint}Don't hold back{/hint} next time. I can handle more than you think."),

            ]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("public_shy"):
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([
                _("I still {hint}blush when I think{/hint} about what we did..."),

                _("{hint}Please don't tell anyone{/hint} about us. I'd die of embarrassment."),

                _("I keep replaying it in my head... {hint}is that weird?{/hint}"),

            ]))
            girl.discover("discovered_trait_public_shy")
        else:
            Say_Line(girl, renpy.random.choice([
                _("So... are we going to pretend that didn't happen?"),
                _("I've been thinking about last time. A lot."),
                _("Things have changed between us, haven't they? I don't mind."),
            ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)
        Change_Status(girl, "Love", 2)

    # --- After BJ history ---
    def chitchat_history_bj(girl, loc, t_index):
        bj_count = get_sex_count(girl, "bj")
        set_scene_expression(girl, "smile")
        if girl.has_trait("cum_slut"):
            Say_Line(girl, renpy.random.choice([
                _("I keep thinking about {hint}how you tasted{/hint}... when can I do it again?"),

                _("My mouth gets {hint}lonely when you're not around{/hint}. Just saying."),

                _("I want to {hint}go down on you again{/hint}. I liked making you feel good."),

            ]))
            girl.discover("discovered_trait_cum_slut")
        elif girl.has_trait("hate_cum"):
            Say_Line(girl, renpy.random.choice([
                _("About last time... {hint}just don't finish in my mouth{/hint}. Ever. Got it?"),

                _("I did that for you, {hint}not because I enjoy it{/hint}. Remember that."),

                _("If we do that again, {hint}you better warn me{/hint} before you're close."),

            ]))
            girl.discover("discovered_trait_hate_cum")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("Was I... okay? Last time, I mean. {hint}When I used my mouth{/hint}."),

                _("{hint}I was so nervous{/hint}... but I wanted to make you happy."),

                _("I've been {hint}practicing{/hint}... no, forget I said that!"),

            ]))
        else:
            if bj_count > 3:
                Say_Line(girl, renpy.random.choice([
                    _("I've gotten pretty good at that, haven't I?"),
                    _("You keep asking for it... not that I'm complaining."),
                    _("At this point I know exactly what you like."),
                ]))
            else:
                Say_Line(girl, renpy.random.choice([
                    _("I still get a little nervous before doing... that."),
                    _("Don't look at me like that. You know what I'm thinking about."),
                    _("My jaw was sore for a whole day after last time, you know."),
                ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # --- After creampie history ---
    def chitchat_history_creampie(girl, loc, t_index):
        cream_count = getattr(girl, "CreampieCounts", 0)
        set_scene_expression(girl, "normal")
        if girl.has_trait("cum_slut"):
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("I still feel warm thinking about when {hint}you finished inside me{/hint}..."),

                _("You know what I want? {hint}I want you to fill me up again{/hint}."),

                _("I've been {hint}craving that feeling{/hint}... you know, when you don't pull out."),

            ]))
            girl.discover("discovered_trait_cum_slut")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("hate_cum"):
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("I'm STILL {hint}upset about you finishing inside me{/hint}. Don't do it again."),

                _("You have no idea how {hint}stressed I was{/hint} after you came inside me."),

                _("If you ever {hint}do that without my permission again, we're done{/hint}."),

            ]))
            girl.discover("discovered_trait_hate_cum")
            Change_Status(girl, "Love", -3)
        elif girl.has_trait("cute_sex"):
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([
                _("When you finished inside me... I was scared, but it also felt... {hint}intimate{/hint}."),

                _("I've been thinking about it. It felt {hint}really close. Really personal{/hint}."),

                _("You promise to be careful, right? {hint}That was a lot to take in{/hint}..."),

            ]))
            girl.discover("discovered_trait_cute_sex")
            Change_Status(girl, "Love", 2)
        else:
            if cream_count > 3:
                Say_Line(girl, renpy.random.choice([
                    _("You really like finishing inside, don't you? I've noticed."),
                    _("At this point I've lost count of how many times you've done it inside me."),
                    _("I should probably be more careful... but I trust you."),
                ]))
            else:
                Say_Line(girl, renpy.random.choice([
                    _("About when you... finished inside me. Are we going to talk about that?"),
                    _("I felt you finish inside me last time. That's... a big deal."),
                    _("You should have asked before doing that inside me. Just saying."),
                ]))
            Change_Status(girl, "Inbt", 3)
        set_scene_expression(girl, "normal")

    # --- After being filmed ---
    def chitchat_history_filmed(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        if girl.has_trait("camera_lover"):
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("So... about that video you took of me. {hint}Did it turn out good?{/hint}"),

                _("I hope you got {hint}my good side{/hint}. I want to see it."),

                _("{hint}Film me again{/hint} sometime. I'll give you a better performance."),

            ]))
            girl.discover("discovered_trait_camera_lover")
            Change_Status(girl, "Inbt", 3)
        elif girl.has_trait("camera_hater"):
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("You better have {hint}deleted that video{/hint}. I'm not joking."),

                _("If that video of me gets out, I swear {hint}I'll make your life hell{/hint}."),

                _("I can't believe you actually recorded that. {hint}I feel violated{/hint}."),

            ]))
            girl.discover("discovered_trait_camera_hater")
            Change_Status(girl, "Love", -5)
        elif girl.has_trait("public_fetish"):
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("The idea that a video of us exists somewhere... {hint}it's exciting{/hint}."),

                _("What if someone accidentally saw that video? {hint}...That thought thrills me{/hint}."),

                _("You could {hint}show it to someone{/hint}. I wouldn't stop you."),

            ]))
            girl.discover("discovered_trait_public_fetish")
            Change_Status(girl, "Inbt", 4)
        elif girl.has_trait("public_shy"):
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("{hint}Promise me{/hint} you haven't shown that video to anyone. Please."),

                _("I get {hint}anxious{/hint} just knowing that recording exists..."),

                _("If anyone ever finds that video, {hint}I would literally die{/hint}."),

            ]))
            girl.discover("discovered_trait_public_shy")
            Change_Status(girl, "Love", -2)
        else:
            Say_Line(girl, renpy.random.choice([
                _("About that video... just be careful with it, okay?"),
                _("I hope you know I don't just let anyone record me like that."),
                _("That video stays between us. I mean it."),
            ]))
            Change_Status(girl, "Inbt", 2)
        set_scene_expression(girl, "normal")

    # --- After raw sex (no condom) history ---
    def chitchat_history_raw_sex(girl, loc, t_index):
        raw_count = getattr(girl, "raw_sex_count", 0)
        set_scene_expression(girl, "normal")
        if girl.has_trait("cum_slut"):
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("I love it when we do it {hint}without anything between us{/hint}."),

                _("{hint}Raw just feels so much better{/hint}. Don't you agree?"),

                _("I don't even want you to {hint}use a condom anymore{/hint}. It ruins it."),

            ]))
            girl.discover("discovered_trait_cum_slut")
        elif girl.has_trait("hate_cum"):
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("I still think we should {hint}always use protection{/hint}. I'm serious."),

                _("Going without a condom makes me {hint}so nervous{/hint}. Next time, use one."),

                _("You keep 'forgetting' condoms. {hint}I'm not stupid{/hint}, you know."),

            ]))
            girl.discover("discovered_trait_hate_cum")
        else:
            if raw_count > 3:
                Say_Line(girl, renpy.random.choice([
                    _("We've been doing it raw a lot... should we talk about that?"),
                    _("I'm getting used to the feeling without a condom. Is that bad?"),
                    _("At some point we should be more responsible... but not today."),
                ]))
            else:
                Say_Line(girl, renpy.random.choice([
                    _("Going without a condom was... different. Intense."),
                    _("I trust you, but we should be more careful next time."),
                    _("The feeling of no barrier... I can't stop thinking about it."),
                ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    # --- After multiple orgasms together ---
    def chitchat_history_orgasm(girl, loc, t_index):
        orgasms = getattr(girl, "Orgasms", {})
        total = sum(orgasms.values())
        fav = getattr(girl, "FavoriteAct", None)
        set_scene_expression(girl, "smile")

        if girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("You've been making me cum so hard lately... {hint}I want more{/hint}."),

                _("Nobody has ever made me finish like you do. {hint}Don't stop{/hint}."),

                _("{hint}I need it rougher{/hint}. Push me harder next time."),

            ]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("You always make me {hint}feel so good{/hint}... it's overwhelming sometimes."),

                _("I feel {hint}safe enough{/hint} with you to really let go. That means a lot."),

                _("You're the only one who {hint}takes the time{/hint} to make me finish. Thank you."),

            ]))
            girl.discover("discovered_trait_cute_sex")
        else:
            if fav and orgasms.get(fav, 0) > 2:
                _fav_names = {
                    "hj": "handjobs", "bj": "blowjobs", "tj": "titjobs",
                    "cowgirl": "riding you", "reverse_cowgirl": "reverse_cowgirl", "masturbate": "touching myself",
                }
                _fn = _fav_names.get(fav, "what we do")
                Say_Line(girl, _tl(_("I think {hint}%s{/hint} is my favorite thing we do together... don't judge me.")) % _fn)
                girl.discover("discovered_fav_act")
            else:
                Say_Line(girl, renpy.random.choice([
                    _("You always know how to finish me off. I appreciate that."),
                    _("I came so hard last time... my legs were shaking."),
                    _("I've never been this satisfied. Just thought you should know."),
                ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)
        Change_Status(girl, "Love", 2)

    # --- After handjob history ---
    def chitchat_history_hj(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        if girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("Was I holding it right last time? {hint}I want to get better{/hint} at it..."),

                _("My hand felt tingly the whole day after {hint}touching you like that{/hint}."),

                _("I liked how you reacted when I touched you. {hint}It made me happy{/hint}."),

            ]))
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("A handjob is {hint}just the appetizer{/hint}. You know what I really want."),

                _("I can do {hint}more than just use my hands{/hint}, you know."),

                _("Next time, {hint}don't settle{/hint} for just my hand. Push for more."),

            ]))
            girl.discover("discovered_trait_hardcore_sex")
        else:
            Say_Line(girl, renpy.random.choice([
                _("I noticed you really liked it when I used my hand on you."),
                _("My grip might be improving. Want to find out?"),
                _("It's funny how something so simple can feel so good."),
            ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    # --- After titjob history ---
    def chitchat_history_tj(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        if girl.has_trait("cum_slut"):
            Say_Line(girl, renpy.random.choice([
                _("I loved feeling you between my breasts... {hint}especially the finish{/hint}."),

                _("Next time, {hint}aim for my face{/hint}. I want to feel it."),

                _("You can {hint}use my chest whenever you want{/hint}. I mean it."),

            ]))
            girl.discover("discovered_trait_cum_slut")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("Using my... chest like that was {hint}embarrassing{/hint}. But I liked your reaction."),

                _("Do guys really like that? {hint}Using a girl's breasts{/hint} like that?"),

                _("I'll do it again if you want... just {hint}don't stare too much{/hint}."),

            ]))
        else:
            Say_Line(girl, renpy.random.choice([
                _("My chest was sore after what we did. Worth it, though."),
                _("I didn't know my breasts could be used like that. You taught me."),
                _("You seemed to really enjoy being between them. Noted."),
            ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # --- BF-aware: after cheating ---
    def chitchat_history_cheating(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        _discover_partner(girl)
        girl.discover("discovered_relationship")
        total_cheats = sum(getattr(girl, "CheatActs", {}).values())
        if total_cheats <= 2:
            Say_Line(girl, renpy.random.choice([
                _tl(_("I can't believe I did that... {hint}my %s has no idea{/hint}.")) % girl.partner_label(),
                _format_partner_line(girl, _("What we did... {hint}it can't happen again{/hint}. %(Pp)s'd be devastated.")),

                _("I feel so {hint}guilty{/hint}. But I also feel... alive. Is that terrible?"),

            ]))
            Change_Status(girl, "Love", 2)
        elif girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([
                _("I'm a terrible person. {hint}I keep coming back to you{/hint} and I can't stop."),

                _format_partner_line(girl, _("%(Pp)s {hint}trusts me completely{/hint}. And I keep betraying that trust with you.")),

                _tl(_("Every time I see my %s, {hint}I feel sick{/hint}. But I still want you.")) % girl.partner_label(),
            ]))
            girl.discover("discovered_trait_loyal")
            Change_Status(girl, "Love", 3)
        else:
            Say_Line(girl, renpy.random.choice([
                _format_partner_line(girl, _("My %(pl)s is {hint}so clueless{/hint}. %(Pp)s has no idea about us.")),
                _format_partner_line(girl, _("Honestly? {hint}What %(pp)s doesn't know won't hurt %(po)s{/hint}.")),
                _("{hint}I've stopped feeling guilty{/hint}. Is that bad? I don't care."),

            ]))
            if girl.has_trait("cheater"):
                girl.discover("discovered_trait_cheater")
            Change_Status(girl, "Inbt", 3)
        set_scene_expression(girl, "normal")

    # ==========================================================
    # RELATIONSHIP-AWARE CHITCHATS
    # ==========================================================

    # ---------- DATING THE PLAYER ----------

    def chitchat_dating_couple_talk(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("So... what are we? I mean, officially..."),
            _("I told my friend about us and she wouldn't stop squealing."),
            _("Is it weird that I like saying 'my boyfriend' out loud?"),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("I just want to make sure we're on the same page."),
            _("I mean, we are together, right? Like, for real?"),
            _("Sorry, I just... I like hearing you say it."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "smile")
        Change_Status(girl, "Love", 3)

    def chitchat_dating_jealousy(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        _lines = [
            _("I saw you talking to that girl earlier. Should I be worried?"),
            _("You've been pretty popular lately... don't forget who your girlfriend is."),
            _("Some girl was looking at you in class today. I noticed."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "sad")
        _follow = [
            _("I'm not jealous or anything. I just... pay attention."),
            _("Sorry. I trust you. I just get weird sometimes."),
            _("Forget I said anything. I'm being silly."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_dating_future_plans(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        _lines = [
            _("Do you think about us in the future?"),
            _("Where do you see us in a year?"),
            _("I wonder what things will be like after college... for us, I mean."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "smile")
        _follow = [
            _("I like imagining it. Is that too much?"),
            _("I don't need a plan. I just want you in it."),
            _("No pressure. I just... think about it sometimes."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)

    def chitchat_dating_pet_names(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("What should I call you? Babe? Honey? ...Master?"),
            _("Do you like pet names? I've been trying some out in my head."),
            _("I almost called you 'babe' in front of everyone today. Close call."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "smirk")
        _follow = [
            _("Don't laugh! I'm serious. Pick one before I pick for you."),
            _("Okay, your face right now tells me you liked 'Master.' Noted."),
            _("Fine, I'll just call you whatever I want. You don't get a vote."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 2)

    # ---------- EX-GIRLFRIEND ----------

    def chitchat_ex_awkward(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        _lines = [
            _("This is weird, isn't it? Us talking like nothing happened."),
            _("I keep expecting it to feel normal, but... it doesn't."),
            _("Funny how we used to talk about everything. Now it's just... this."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("I guess we just pretend everything's fine?"),
            _("Sorry. I don't know how to act around you anymore."),
            _("Let's just... try to be normal. Whatever that means now."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_ex_regret(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        _lines = [
            _("You know, I still think about what you did."),
            _("I tried not to be bitter, but some days it just hits me."),
            _("Every time I see you, I remember why we didn't work out."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "sad")
        _follow = [
            _("Maybe one day I'll stop caring. Today isn't that day."),
            _("I'm not trying to start a fight. I just... needed to say that."),
            _("Forget it. It doesn't matter anymore. Or it shouldn't."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", -1)

    def chitchat_ex_moving_on(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("I'm doing fine without you, just so you know."),
            _("Life's actually been pretty good since... you know."),
            _("I've been focusing on myself lately. It feels nice, actually."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("Not that I need to prove anything to you."),
            _("I just wanted you to know I'm not some sad ex moping around."),
            _("Anyway. How have you been? ...Wait, do I even want to know?"),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_ex_second_chances(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        _lines = [
            _("Do you ever wonder if we made a mistake?"),
            _("Sometimes I catch myself thinking about how things used to be."),
            _("I had a dream about us the other night. The old us."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("Forget I said that. It doesn't mean anything."),
            _("I'm not saying I want to try again. I'm just... thinking out loud."),
            _("People change, right? Maybe we both have."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    # ---------- HAS NPC BOYFRIEND ----------

    def chitchat_npc_bf_sweet(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _pf = partner_fmt(girl)
        _lines = [
            _("My %(pl)s texted me today... %(pp)s's so sweet."),
            _("My %(pl)s surprised me with flowers yesterday. Out of nowhere."),
            _("I was on the phone with my %(pl)s earlier. %(Pp)s always makes me laugh."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)) % _pf)
        set_scene_expression(girl, "normal")
        _pf2 = _pf
        _follow = [
            _("Sorry, I didn't mean to go on about %(po)s. How's your love life?"),
            _("Anyway, enough about me. What's new with you?"),
            _("I know, I know. I'm being one of those people. Sorry."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)) % _pf2)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    def chitchat_npc_bf_advice(girl, loc, t_index):
        _npc = get_npc_partner_for(girl)
        _pname = getattr(_npc, "name", None) or getattr(girl, "_npc_partner_name", None)
        _pl = girl.partner_label() if hasattr(girl, "partner_label") else "partner"

        set_scene_expression(girl, "normal")
        _lines = [
            _("Can I ask you something about relationships?"),
            _("You seem like someone who'd give good advice. About relationships, I mean."),
            _("I need an outside perspective on something. You free to listen?"),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "sad")
        _pf = dict(partner_fmt(girl), pname=_pname or _pl)
        _follow = [
            _("When %(pname)s stops texting as much... does that mean something?"),
            _("Is it normal for things to feel kind of routine after a while?"),
            _("How do you know if someone's losing interest? Asking for a friend."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)) % _pf)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    def chitchat_npc_bf_doubts(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        _pf = partner_fmt(girl)
        _lines = [
            _("Sometimes I wonder if I'm with the right person..."),
            _("Is it bad that I keep comparing my %(pl)s to other people?"),
            _("I love my %(pl)s. At least... I think I do. Is that bad?"),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)) % _pf)
        set_scene_expression(girl, "normal")
        _follow = [
            _("Sorry, that was heavy. Just ignore me."),
            _("Don't tell anyone I said that. I'm just in a weird mood."),
            _("Maybe I'm overthinking it. Relationships are hard."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 1)

    def chitchat_npc_bf_comparing(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _pf = partner_fmt(girl)
        _lines = [
            _("You know, you're actually pretty easy to talk to. Unlike some people."),
            _("I wish my %(pl)s was as easy to talk to as you are."),
            _("How come you always know what to say? My %(pl)s could learn a thing or two."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)) % _pf)
        set_scene_expression(girl, "embarrassed")
        _follow = [
            _("Wait, don't read into that. I didn't mean it like that."),
            _("I'm just saying you're a good listener. That's all. Stop looking at me like that."),
            _("Forget I said that. I'm not comparing. ...Okay, maybe a little."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 2)

    # ---------- HIGH LOVE, NOT DATING ----------

    def chitchat_high_love_hints(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("You know, I really enjoy spending time with you..."),
            _("I always look forward to seeing you. More than I probably should."),
            _("It's funny... you're the first person I think about when something good happens."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("I wonder why that is."),
            _("Anyway, just thought you should know."),
            _("Don't make it weird. I'm just being honest."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)

    def chitchat_high_love_frustration(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        _lines = [
            _("Are you ever going to make a move or what?"),
            _("Seriously, how many hints do I have to drop?"),
            _("I'm starting to think you're either oblivious or just enjoying watching me squirm."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "sad")
        _follow = [
            _("Forget it. I didn't say anything."),
            _("I'm not desperate. I'm just... tired of waiting."),
            _("If you don't feel the same way, just tell me. I can take it."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 2)

    def chitchat_high_love_flirty(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("If you asked me out, I definitely wouldn't say no. Just saying."),
            _("You know, a girl can only wait so long before she gives up..."),
            _("I keep daydreaming about us together. Don't tell anyone."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("Ball's in your court. Just so you know."),
            _("I'm not going to spell it out for you. Figure it out."),
            _("...Or maybe I'm just messing with you. You'll never know."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "smile")
        Change_Status(girl, "Love", 3)
        Change_Status(girl, "Inbt", 3)

    # ---------- LOW LOVE ----------

    def chitchat_low_love_cold(girl, loc, t_index):
        set_scene_expression(girl, "angry")
        _lines = [
            _("I don't really have much to say to you right now."),
            _("Look, I'm not in the mood for small talk."),
            _("Can you not? I'm really not feeling chatty today."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("Nothing personal. Or maybe it is. Who knows."),
            _("Just go bother someone else for a bit."),
            _("We're done here, right?"),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")

    def chitchat_low_love_distant(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        _lines = [
            _("Can we keep this short? I'm busy."),
            _("Yeah, hi. Was there something you needed?"),
            _("Oh, it's you. I was just heading out, actually."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "sad")
        _follow = [
            _("Sorry, I don't mean to be rude. I just... have stuff going on."),
            _("Maybe we can talk later. Or not. Whatever."),
            _("I've got things to do. Catch you around, I guess."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        set_scene_expression(girl, "normal")

    # ==========================================================
    # WITNESS HISTORY HELPERS
    # ==========================================================

    def _witness_entries(girl):
        """Return the girl's witness_history list (safe fallback)."""
        return getattr(girl, "witness_history", []) or []

    def _has_witness_type(girl, cheat_type):
        """True if any witness entry matches the given cheating_type."""
        return any(e.get("cheating_type") == cheat_type for e in _witness_entries(girl))

    def _has_witness_act(girl, act):
        """True if any witness entry has this act type."""
        return any(e.get("act") == act for e in _witness_entries(girl))

    def _has_witness_public(girl):
        """True if any witness entry happened in a public location."""
        return any(e.get("is_public", False) for e in _witness_entries(girl))

    def _has_witness_location(girl, loc):
        """True if any witness entry happened at a specific location."""
        return any(e.get("location") == loc for e in _witness_entries(girl))

    def _witness_count(girl):
        """Total number of witness entries."""
        return len(_witness_entries(girl))

    # ==========================================================
    # WITNESS CHITCHAT TOPICS
    # ==========================================================

    # ── She was cheated on (witness_was_cheated_on) ──

    def chitchat_witness_cheated_on(girl, loc, t_index):
        """Girl talks about catching the player cheating on her."""
        set_scene_expression(girl, "angry")

        if girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([
                _("I gave you everything. My trust, my loyalty. And you threw it in my face."),
                _("I was the one who would never cheat. You couldn't say the same, could you?"),
                _("Do you know what it's like to be faithful and then see THAT?"),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I still think about it. Every single day."),
                _("I don't know if I'll ever trust someone the same way again."),
                _("The worst part is... I still care about you. And I hate myself for it."),
            ]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("You had the nerve to do that where I could see? Bold. Stupid, but bold."),
                _("I'm not some doormat you can walk over and expect to stay quiet."),
                _("If you wanted someone else, you should have said so instead of sneaking around."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I'm not crying over it. But don't think I've forgotten."),
                _("You'll have to work a LOT harder if you want me back."),
            ]))
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("I keep replaying it in my head... you with her... it hurts so much."),
                _("I thought we had something special. Was I wrong about everything?"),
                _("Every time I close my eyes, I see it. You and her together."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I just want to understand why. Was I not enough?"),
                _("I'm trying to move on, but it's so hard when I see you every day."),
                _("Maybe I was naive to think you'd only want me..."),
            ]))
        else:
            Say_Line(girl, renpy.random.choice([
                _("I saw what you did. Don't pretend like it didn't happen."),
                _("You really thought I wouldn't find out? Or did you just not care?"),
                _("Catching you with her was the worst moment of my life here."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I'm still processing it, honestly."),
                _("I don't know where we stand anymore. And that scares me."),
                _("Just tell me one thing. Did she mean more to you than I did?"),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", -3)

    # ── She saw another girl cheating on her BF (witness_saw_girl_cheat) ──

    def chitchat_witness_saw_girl_cheat(girl, loc, t_index):
        """Girl comments on seeing another girl cheat on her partner with the player."""
        set_scene_expression(girl, "normal")

        if girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([
                _("I can't believe she did that to her partner. That's disgusting."),
                _("She has someone who loves her and she does THAT behind their back?"),
                _("I would never do that to someone I'm with. What she did is unforgivable."),
            ]))
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("And you just went along with it. Doesn't that bother you at all?"),
                _("Her partner deserves to know."),
                _("I hope you know what kind of person she really is."),
            ]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("cheater"):
            Say_Line(girl, renpy.random.choice([
                _("So she's got a partner and she's with you? Smart girl."),
                _("Honestly? Her partner probably isn't giving her what she needs."),
                _("I'm not one to judge. People have needs."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("Just be careful. If her partner finds out, it won't be pretty."),
                _("Maybe she and I have more in common than I thought."),
                _("As long as nobody gets caught, what's the harm?"),
            ]))
            girl.discover("discovered_trait_cheater")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("Wait, she has a partner? And you two were... oh my god."),
                _("That's so wrong. Her poor partner has no idea..."),
                _("I feel bad just knowing about it. Should I say something?"),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I don't want to get involved, but it feels wrong to stay quiet."),
                _("Promise me you'd never do that to someone who trusts you."),
                _("I couldn't live with that kind of guilt..."),
            ]))
        elif girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([
                _("The fact that she did it where someone could see... that takes nerve."),
                _("I won't lie, there's something thrilling about the risk of getting caught."),
                _("Her partner would lose it if they knew. And honestly, that's kind of exciting."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("Not saying I approve. Just saying I understand the rush."),
                _("The danger makes it hotter, doesn't it? Don't look at me like that."),
            ]))
            girl.discover("discovered_trait_public_fetish")
        else:
            Say_Line(girl, renpy.random.choice([
                _("So I saw you with her the other day. Does her partner know?"),
                _("She's got a partner and she's sneaking around with you? Yikes."),
                _("I'm not going to tell anyone, but... that's messy."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("Just be careful. These things always come out eventually."),
                _("I'm staying out of it, but don't drag me into your drama."),
                _("None of my business, I guess. But still... wow."),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    # ── She saw both cheating (witness_saw_both_cheat) ──

    def chitchat_witness_saw_both_cheat(girl, loc, t_index):
        """Girl witnessed player cheating on her AND the other girl cheating on her partner."""
        set_scene_expression(girl, "angry")

        if girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([
                _("You cheated on me with a girl who's ALSO cheating on her partner? You're both terrible."),
                _("So neither of you has any loyalty. Great. That makes me feel SO much better."),
                _("I was the only one being faithful in any of this. What a joke."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I feel like an idiot for trusting either of you."),
                _("Two cheaters found each other. I should have seen it coming."),
                _("At least I know now. I won't make that mistake again."),
            ]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("You and her deserve each other. Two backstabbers in one room."),
                _("You couldn't even cheat with someone single? Real classy."),
                _("Her partner and I both got screwed over. Not the fun kind either."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I'm done being angry about it. But I'm NEVER forgetting it."),
                _("Next time, don't make promises you can't keep."),
            ]))
        else:
            Say_Line(girl, renpy.random.choice([
                _("You cheated on me, and she's cheating on her partner. What a mess."),
                _("So I walked in on two people who don't care about anyone but themselves."),
                _("Her partner doesn't know, I didn't know. Real nice."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I just keep asking myself why. Why wasn't I enough?"),
                _("I hope it was worth it. For both of you."),
                _("I don't even know who to be more angry at. You or her."),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", -5)

    # ── She saw it happen in public ──

    def chitchat_witness_public(girl, loc, t_index):
        """Girl comments on witnessing acts in a public place."""
        set_scene_expression(girl, "startled")

        if girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([
                _("I still think about seeing you two out in the open like that. It was... exciting."),
                _("You really went for it in public. That takes courage. Or insanity."),
                _("The fact that anyone could have walked by and seen you two... my heart was racing."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("If that ever happens again, maybe give me a heads up first. I might want a better view."),
                _("I won't lie, I've been thinking about what I saw more than I should."),
                _("You know, I wouldn't mind being in that situation myself someday."),
            ]))
            girl.discover("discovered_trait_public_fetish")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("public_shy"):
            Say_Line(girl, renpy.random.choice([
                _("I can't believe you did that where ANYONE could see! What is wrong with you?!"),
                _("Do you have any idea how embarrassing it was to walk in on that?"),
                _("I still get red just thinking about it. In PUBLIC? Really?"),
            ]))
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("If someone else had seen... I don't even want to think about it."),
                _("Please, for the love of everything, get a room next time."),
                _("I'm traumatized. Genuinely traumatized."),
            ]))
            girl.discover("discovered_trait_public_shy")
            Change_Status(girl, "Love", -2)
        elif girl.has_trait("voyeur"):
            Say_Line(girl, renpy.random.choice([
                _("I couldn't look away when I saw you two. I know I should have, but..."),
                _("You were right there, out in the open. I watched longer than I should admit."),
                _("The thrill of watching you without you knowing... I'm not proud of it."),
            ]))
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([
                _("Don't tell anyone I said that. I have a reputation to maintain."),
                _("I know it's weird. But I couldn't help myself."),
                _("Next time... maybe don't be so careless. Or do. Your call."),
            ]))
            girl.discover("discovered_trait_voyeur")
            Change_Status(girl, "Inbt", 4)
        else:
            Say_Line(girl, renpy.random.choice([
                _("You know I saw you two outside, right? You weren't exactly subtle."),
                _("Anyone could have seen what you were doing. Were you trying to get caught?"),
                _("Doing that out in the open... do you just not care who sees?"),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I'm not judging. Okay, maybe a little. But seriously, be more careful."),
                _("Just keep it behind closed doors next time, alright?"),
                _("I'll pretend I didn't see anything. You're welcome."),
            ]))

        set_scene_expression(girl, "normal")

    # ── She saw it at a specific location (pool) ──

    def chitchat_witness_pool(girl, loc, t_index):
        """Girl comments on seeing acts at the pool."""
        set_scene_expression(girl, "startled")

        if girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([
                _("At the pool? With people potentially around? You've got serious nerve."),
                _("The pool, of all places... the water, the swimsuits... it was like a scene from a movie."),
                _("I still think about what I saw by the pool. The wet skin, the heat... wow."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("Maybe we should go swimming together sometime. See what happens."),
                _("The pool is never going to feel the same after what I saw."),
            ]))
            girl.discover("discovered_trait_public_fetish")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("The pool?! Someone could have been swimming right there!"),
                _("I went to the pool to relax and instead I saw... THAT."),
                _("I can never go back to the pool without thinking about what I saw..."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("It was so embarrassing. I almost tripped running away."),
                _("Please tell me that was a one-time thing..."),
            ]))
            Change_Status(girl, "Love", -1)
        else:
            Say_Line(girl, renpy.random.choice([
                _("The pool? Seriously? That's bold even by your standards."),
                _("I went for a swim and got a show I didn't ask for."),
                _("You do know other people use that pool, right?"),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I'm trying to forget what I saw, but it's not working."),
                _("Next time, at least check if anyone is coming first."),
                _("I'll never look at the pool the same way again."),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    # ── She saw it at a specific location (shower) ──

    def chitchat_witness_shower(girl, loc, t_index):
        """Girl comments on seeing acts in the shower area."""
        set_scene_expression(girl, "startled")

        if girl.has_trait("voyeur"):
            Say_Line(girl, renpy.random.choice([
                _("I walked past the showers and heard... things. So I stopped. And listened."),
                _("The shower steam made everything look so... intense. I couldn't look away."),
                _("I saw more than I should have in those showers. And I don't regret it one bit."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("The acoustics in there are... really something. Every sound was crystal clear."),
                _("If you ever need someone to wash your back, I volunteer."),
            ]))
            girl.discover("discovered_trait_voyeur")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("public_shy"):
            Say_Line(girl, renpy.random.choice([
                _("The showers?! Those doors don't even LOCK properly!"),
                _("I needed to shower and instead I walked into your... performance."),
                _("I was SO embarrassed. I dropped my towel and ran."),
            ]))
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("I couldn't shower for two days because I was too scared to go back."),
                _("Lock the door next time! If there even IS a lock!"),
            ]))
            girl.discover("discovered_trait_public_shy")
            Change_Status(girl, "Love", -2)
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("The shower, huh? At least you picked somewhere with easy cleanup."),
                _("I heard the water running for WAY too long. Now I know why."),
                _("Showers are practical for that kind of thing. Not judging."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("Next time, run the water louder. I could hear everything."),
                _("Just saying... the acoustics in that shower leave nothing to the imagination."),
            ]))
            Change_Status(girl, "Inbt", 3)
        else:
            Say_Line(girl, renpy.random.choice([
                _("I walked into the showers and got a LOT more than I bargained for."),
                _("You were in the shower with her. I saw. End of story."),
                _("The shower area is shared, you know. Some of us actually use it to shower."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I'm going to need some time before I can shower in peace again."),
                _("At least put a towel on the door handle or something. A warning."),
                _("I'll knock from now on. Trust me."),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    # ── She saw it in a bedroom/room ──

    def chitchat_witness_bedroom(girl, loc, t_index):
        """Girl comments on seeing acts in a bedroom."""
        set_scene_expression(girl, "normal")

        if girl.has_trait("voyeur"):
            Say_Line(girl, renpy.random.choice([
                _("The door was cracked open. I didn't mean to look, but... I did."),
                _("I heard noises from your room. I stood outside longer than I should have."),
                _("I peeked through the door. I know it's wrong. But I couldn't help it."),
            ]))
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([
                _("You should really close your door all the way. Or don't. Up to you."),
                _("I might have seen everything. I might have seen nothing. You'll never know."),
            ]))
            girl.discover("discovered_trait_voyeur")
            Change_Status(girl, "Inbt", 4)
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("I came to your room to ask you something and... the door was open..."),
                _("I didn't mean to see anything! I just knocked and it swung open!"),
                _("I've been avoiding your hallway since that day. You know why."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("The image is burned into my brain. I can't unsee it."),
                _("Please just lock your door from now on. For both our sakes."),
                _("I knocked! I swear I knocked!"),
            ]))
        elif girl.has_trait("cheater"):
            Say_Line(girl, renpy.random.choice([
                _("I caught a glimpse when I walked by your room. Nice moves."),
                _("Your room, huh? At least you keep it behind closed doors. Mostly."),
                _("I wasn't snooping. The door was open. Not my fault I have eyes."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("Looked like fun. Maybe I should swing by more often."),
                _("Don't worry, your secret is safe with me. I've got my own."),
            ]))
            girl.discover("discovered_trait_cheater")
            Change_Status(girl, "Inbt", 3)
        else:
            Say_Line(girl, renpy.random.choice([
                _("I accidentally walked in on you in your room. I'm still recovering."),
                _("Your door wasn't fully closed and I saw way more than I wanted to."),
                _("Next time you're... busy... maybe lock the door?"),
            ]))
            set_scene_expression(girl, "startled")
            Say_Line(girl, renpy.random.choice([
                _("I knocked. I really did. It just... opened."),
                _("I'll text before coming over from now on. Lesson learned."),
                _("Let's just pretend that never happened. Deal?"),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 2)

    # ── She watched the whole thing ──

    def chitchat_witness_watched(girl, loc, t_index):
        """Girl comments on having stayed and watched."""
        set_scene_expression(girl, "shy")

        if girl.has_trait("voyeur"):
            Say_Line(girl, renpy.random.choice([
                _("Remember when I watched you two? I still think about it sometimes."),
                _("I know it's weird that I stayed and watched. But I couldn't look away."),
                _("Watching you with her was... educational. Among other things."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("If you ever need an audience again, you know where to find me."),
                _("I learned a few things just from watching. Want me to demonstrate?"),
                _("Honestly, it was the hottest thing I've ever seen. Don't let it go to your head."),
            ]))
            girl.discover("discovered_trait_voyeur")
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Lust", 5)
        elif girl.has_trait("exhibitionist"):
            Say_Line(girl, renpy.random.choice([
                _("Seeing you with her made me realize something about myself."),
                _("I stayed and watched because... I liked the idea of being seen too."),
                _("If I was the one with you, I wouldn't mind someone watching us."),
            ]))
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("Maybe that makes me weird. Or maybe it makes me honest."),
                _("Next time, let ME be the one putting on the show."),
            ]))
            girl.discover("discovered_trait_exhibitionist")
            Change_Status(girl, "Inbt", 5)
        else:
            Say_Line(girl, renpy.random.choice([
                _("I don't know why I stayed and watched you two. I just... froze."),
                _("I should have left but my feet wouldn't move. I saw everything."),
                _("I keep telling myself I should have walked away. But I didn't."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("It's been on my mind ever since. I can't shake it."),
                _("Can we just not talk about the fact that I stood there watching?"),
                _("I'm not that kind of person. Usually. That night was... different."),
            ]))
            Change_Status(girl, "Inbt", 3)

        set_scene_expression(girl, "normal")

    # ── She joined the session ──

    def chitchat_witness_joined(girl, loc, t_index):
        """Girl comments on having joined a session."""
        set_scene_expression(girl, "smile")

        # taking the lead is femdom, not hardcore (docs/plan_femdom.md D3)
        if girl.has_trait("femdom"):
            Say_Line(girl, renpy.random.choice([
                _("That threesome was intense. We should do it again."),
                _("Joining you two was the best decision I've made in a while."),
                _("I've been thinking about how to top what we did together."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("Next time, I want to take the lead. You two just keep up."),
                _("Round two happens on my schedule. You'll both do what I say."),
                _("Next round, I set the pace. For both of you."),
            ]))
            girl.discover("discovered_trait_femdom")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([
                _("That threesome was intense. We should do it again."),
                _("Joining you two was the best decision I've made in a while."),
                _("I've been thinking about how to top what we did together."),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("I hope she's up for round two. Because I definitely am."),
                _("Next time, I want it rougher. Way rougher."),
            ]))
            girl.discover("discovered_trait_hardcore_sex")
            Change_Status(girl, "Inbt", 5)
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("I can't believe I actually joined you two... that was so unlike me."),
                _("My heart was pounding the whole time. I've never done anything like that."),
                _("I'm still not sure what came over me. But I don't regret it. Mostly."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("Promise me you won't tell anyone. I'd die of embarrassment."),
                _("It was special, right? Not just... meaningless?"),
                _("Can we just keep that between us? Please?"),
            ]))
            Change_Status(girl, "Love", 3)
        elif girl.has_trait("cheater") and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            Say_Line(girl, renpy.random.choice([
                _format_partner_line(girl, _("My %(pl)s doesn't know I joined you two. And %(pp)s never will.")),
                _tl(_("That was wild. Two people at once. My %s could never.")) % girl.partner_label(),
                _format_partner_line(girl, _("Joining you and her was the most exciting thing I've done behind %(poss)s back.")),
            ]))
            set_scene_expression(girl, "sly")
            Say_Line(girl, renpy.random.choice([
                _("Let me know next time. I'll clear my schedule."),
                _format_partner_line(girl, _("%(Pp)s thinks I was studying. If only %(pp)s knew.")),
            ]))
            girl.discover("discovered_trait_cheater")
            Change_Status(girl, "Inbt", 4)
        else:
            Say_Line(girl, renpy.random.choice([
                _("About the time I joined you two... that was something else."),
                _("I never thought I'd be the type to join a... you know. But here we are."),
                _("Three people. One room. I still can't believe that happened."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("It was fun, though. I won't deny that."),
                _("Are we ever going to talk about it? Or just pretend it didn't happen?"),
                _("If the opportunity comes up again... I might say yes. Maybe."),
            ]))
            Change_Status(girl, "Inbt", 3)

        set_scene_expression(girl, "normal")

    # ── She left embarrassed ──

    def chitchat_witness_embarrassed(girl, loc, t_index):
        """Girl talks about having left embarrassed after seeing the player."""
        set_scene_expression(girl, "sad")

        if girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _("I'm still mortified about walking in on you. I couldn't sleep that night."),
                _("Every time I see you now, my face turns red and I think about THAT."),
                _("I've been going out of my way to avoid running into you since... you know."),
            ]))
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("It's YOUR fault for not locking the door!"),
                _("A little warning would have been nice! A sock on the door, anything!"),
                _("I can never look at you the same way again. Thanks for that."),
            ]))
        elif girl.has_trait("public_shy"):
            Say_Line(girl, renpy.random.choice([
                _("I literally ran away when I saw you. My legs moved before my brain did."),
                _("The image is seared into my memory. I wish I could delete it."),
                _("I've been taking longer routes to avoid that spot ever since."),
            ]))
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("Do you have ANY idea how mortifying that was for me?"),
                _("If anyone else had seen me seeing you... I would have died on the spot."),
            ]))
            girl.discover("discovered_trait_public_shy")
        else:
            Say_Line(girl, renpy.random.choice([
                _("That was really awkward the other day. Walking in on you like that."),
                _("I've been avoiding you a little since... the incident."),
                _("I didn't mean to see anything. But I definitely saw something."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("Let's just move past it. Pretend it never happened."),
                _("I'm over it. Mostly. Just warn me next time."),
                _("We're adults, right? These things happen. It's fine. Totally fine."),
            ]))

        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    # ==========================================================
    # PLAYER-GF CHEATING PROGRESSION CHITCHATS
    # Girl comments on helping the player cheat on his girlfriend.
    # Uses PlayerCheatCount to escalate the tone.
    # ==========================================================

    def chitchat_pgf_cheat_first(girl, loc, t_index):
        """After first time cheating on player's GF with this girl."""
        gf_name = _get_player_gf_name()
        set_scene_expression(girl, "worried")

        if girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([
                _tl(_("I keep thinking about what we did... %s trusts you. And I helped you betray her.")) % gf_name,
                _tl(_("I haven't been able to sleep... what we did to %s was terrible. I feel so guilty.")) % gf_name,
                _tl(_("Do you even feel bad about what we did? Because I can't stop thinking about %s...")) % gf_name,
            ]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("cheater"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _("So... are we going to pretend that never happened? Because I don't want to~"),
                _tl(_("I keep replaying what we did... right behind %s's back. It was exciting.")) % gf_name,
                _tl(_("Tell me... does %s have any idea? The secret makes it so much better.")) % gf_name,
            ]))
            girl.discover("discovered_trait_cheater")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([
                _tl(_("I've been thinking about what happened between us... %s can never know. Promise me.")) % gf_name,
                _tl(_("I feel terrible about %s... but I also can't stop thinking about you.")) % gf_name,
                _("What we did was wrong... right? Then why do I want it to happen again...?"),
            ]))
        elif girl.has_trait("public_shy"):
            Say_Line(girl, renpy.random.choice([
                _tl(_("What if someone saw us? What if %s finds out? I'm so scared...")) % gf_name,
                _tl(_("I keep checking if %s is looking at me weird... does she know?")) % gf_name,
            ]))
            girl.discover("discovered_trait_public_shy")
        elif girl.has_trait("exhibitionist"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("Part of me wants %s to find out... is that messed up?")) % gf_name,
                _("I almost wish someone had seen us... the danger was the best part."),
                _tl(_("The fact that %s could walk in at any moment made it so much hotter.")) % gf_name,
            ]))
            girl.discover("discovered_trait_exhibitionist")
        elif girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _tl(_("What we did was intense... and the fact that %s has no idea makes it better.")) % gf_name,
                _tl(_("I don't feel bad. If %s can't keep you satisfied, someone else will.")) % gf_name,
                _tl(_("If you're going to cheat on %s... at least you picked someone worth it.")) % gf_name,
            ]))
        else:
            Say_Line(girl, renpy.random.choice([
                _tl(_("About what happened... %s can't find out. You know that, right?")) % gf_name,
                _tl(_("I've been thinking about us... and about %s. She doesn't deserve this.")) % gf_name,
                _tl(_("Just so we're clear... that was a one-time thing. %s can never know.")) % gf_name,
            ]))

        set_scene_expression(girl, "normal")

    def chitchat_pgf_cheat_recurring(girl, loc, t_index):
        """After multiple times cheating (2-4 count)."""
        gf_name = _get_player_gf_name()
        _pcc = int(getattr(girl, "PlayerCheatCount", 0))

        if girl.has_trait("loyal"):
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _tl(_("We keep doing this... %s is going to find out eventually. And it'll destroy her.")) % gf_name,
                _("Every time I say 'last time'... and then you come back. I'm a terrible person."),
                _tl(_("I look at %s and I feel sick. She has no idea what I've been doing with you.")) % gf_name,
            ]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("cheater"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("How many times now? %s still has no clue~ We're getting good at this.")) % gf_name,
                _tl(_("Every time is better than the last. Poor %s doesn't know what she's missing.")) % gf_name,
                _tl(_("At this point, I'm basically your second girlfriend. %s just doesn't know~")) % gf_name,
            ]))
            girl.discover("discovered_trait_cheater")
        elif girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("We keep coming back to each other. %s clearly isn't enough for you.")) % gf_name,
                _tl(_("I've stopped feeling guilty. If %s can't keep you satisfied, that's her problem.")) % gf_name,
            ]))
        elif girl.has_trait("cute_sex"):
            set_scene_expression(girl, "worried")
            Say_Line(girl, renpy.random.choice([
                _("I told myself never again... but here we are. What's wrong with me?"),
                _tl(_("We can't keep doing this to %s... but I don't want to stop either.")) % gf_name,
                _("I'm falling for you more every time... and I hate myself for it."),
            ]))
        elif girl.has_trait("public_fetish"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _("We've done it multiple times now... and the thrill of getting caught never gets old."),
                _tl(_("Every time we do it somewhere risky, I imagine %s walking in. It's terrifying and amazing.")) % gf_name,
                _tl(_("The more we do this, the more public I want it. Let %s find us. I don't care anymore.")) % gf_name,
            ]))
            girl.discover("discovered_trait_public_fetish")
        elif girl.has_trait("cum_slut"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("I can't help it... every time you come to me, I just want more. %s isn't giving you enough.")) % gf_name,
                _tl(_("Does %s let you do what I let you do? I doubt it~")) % gf_name,
                _tl(_("I keep thinking about the taste of you... while %s has no clue.")) % gf_name,
            ]))
            girl.discover("discovered_trait_cum_slut")
        elif girl.has_trait("voyeur"):
            set_scene_expression(girl, "worried")
            Say_Line(girl, renpy.random.choice([
                _tl(_("Sometimes I wonder what you do with %s... and I get jealous. And turned on.")) % gf_name,
                _("I keep imagining you with her... and then coming to me right after. It's so wrong."),
                _tl(_("Do you think about me when you're with %s? Because I think about you two together...")) % gf_name,
            ]))
            girl.discover("discovered_trait_voyeur")
        else:
            set_scene_expression(girl, "worried")
            Say_Line(girl, renpy.random.choice([
                _tl(_("%s is going to find out if we keep doing this... are you okay with that?")) % gf_name,
                _("This isn't a one-time thing anymore. We need to talk about what this means."),
                _tl(_("How long do you think we can keep this from %s?")) % gf_name,
                _("Every time I tell myself it's the last time. I'm running out of excuses."),
            ]))

        set_scene_expression(girl, "normal")

    def chitchat_pgf_cheat_veteran(girl, loc, t_index):
        """After many times cheating (5+ count) — normalized, possessive."""
        gf_name = _get_player_gf_name()

        if girl.has_trait("cheater"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("You should just dump %s already. We both know who you really want.")) % gf_name,
                _tl(_("I wonder if %s knows she's sharing you. Probably not. That's the fun part~")) % gf_name,
                _tl(_("At this point, you're basically mine. %s is just a placeholder.")) % gf_name,
            ]))
            girl.discover("discovered_trait_cheater")
        elif girl.has_trait("loyal"):
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I've become the person I always hated... the other woman. And I can't even stop."),
                _("I used to judge girls who did this. Now I AM one. What have you done to me?"),
                _tl(_("I love you... but I hate what we're doing to %s. She deserves better.")) % gf_name,
            ]))
            girl.discover("discovered_trait_loyal")
        # telling him to dump her / what he wants is femdom, not hardcore (docs/plan_femdom.md D3)
        elif girl.has_trait("femdom"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _("Just break up with her already. You've been coming to me for weeks."),
                _("Stop pretending. You want me. You've always wanted me."),
                _tl(_("Here's what happens next. You tell %s it's over, and you do it this week.")) % gf_name,
            ]))
            girl.discover("discovered_trait_femdom")
        elif girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("%s can't give you what I can. We both know it.")) % gf_name,
                _tl(_("With %s it must feel like a warm-up. With me you actually break a sweat.")) % gf_name,
            ]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            set_scene_expression(girl, "worried")
            Say_Line(girl, renpy.random.choice([
                _("I know this is wrong... but I've fallen for you. I can't let go anymore."),
                _tl(_("Every time I see you with %s... it hurts. When will you choose me?")) % gf_name,
                _("I'm in love with someone else's boyfriend... and I don't even want to stop."),
            ]))
        elif girl.has_trait("exhibitionist"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("Honestly? I want %s to catch us. I want her to see what she's losing.")) % gf_name,
                _("We've done it so many times... I'm not even hiding it anymore. Let people see."),
                _tl(_("The whole campus probably knows by now. And I don't care. %s will find out eventually.")) % gf_name,
            ]))
            girl.discover("discovered_trait_exhibitionist")
        elif girl.has_trait("camera_hater"):
            set_scene_expression(girl, "worried")
            Say_Line(girl, renpy.random.choice([
                _tl(_("Promise me there's no evidence of us. If %s ever finds photos or messages...")) % gf_name,
                _tl(_("Delete everything. Every text, every call. %s can NEVER have proof.")) % gf_name,
                _tl(_("I'm paranoid that someone recorded us at some point... %s would destroy me.")) % gf_name,
            ]))
            girl.discover("discovered_trait_camera_hater")
        elif girl.has_trait("public_fetish"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("We've done it everywhere at this point... %s has walked past every place we've been together.")) % gf_name,
                _tl(_("Next time, I want to do it somewhere %s goes every day. Mark my territory~")) % gf_name,
                _("The risk stopped being scary a long time ago. Now it's just fuel."),
            ]))
            girl.discover("discovered_trait_public_fetish")
        elif girl.has_trait("cum_slut"):
            set_scene_expression(girl, "smirk")
            Say_Line(girl, renpy.random.choice([
                _tl(_("Does %s swallow? Because I do. Every. Single. Time.")) % gf_name,
                _tl(_("You keep coming back to me because %s doesn't give you everything. I do~")) % gf_name,
                _tl(_("I know why you cheat on %s. She can't handle you like I can.")) % gf_name,
            ]))
            girl.discover("discovered_trait_cum_slut")
        else:
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _tl(_("At this point, you should just be honest with %s. Or with me.")) % gf_name,
                _("I stopped counting how many times. This is just... us now."),
                _tl(_("You keep coming back. I keep saying yes. %s keeps not knowing.")) % gf_name,
                _("When are you going to make a decision? Her or me?"),
            ]))

        set_scene_expression(girl, "normal")

    # ==========================================================
    # COMPLIMENT BODY AWARENESS (tits/ass)
    # ==========================================================

    # --- She knows he keeps thinking about her ass/tits ---
    def chitchat_knows_thinking_tits(girl, loc, t_index):
        if getattr(girl, "bust", "medium") == "small":
            set_scene_expression(girl, "surprised")
            Say_Line(girl, renpy.random.choice([
                _("Wait... you actually think about my chest? Like, for real?"),
                _("I catch you looking sometimes and I'm like... really? At these?"),
                _("You keep looking at my chest and I honestly don't get it."),
            ]))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 3)
        else:
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("I notice the way you look at my chest, you know."),
                _("I know you keep thinking about grabbing my tits."),
                _("Every time you compliment my chest, I catch you staring right after."),
                _("You are not subtle at all when you look at my breasts."),
            ]))
            Change_Status(girl, "Inbt", 3)
        set_scene_expression(girl, "normal")

    def chitchat_knows_thinking_ass(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, renpy.random.choice([
            _("I can feel your eyes on my ass every time I walk past you."),
            _("I know you keep thinking about grabbing my ass."),
            _("You complimented my butt and now you can not stop looking, can you?"),
            _("I know exactly where your eyes go when I turn around."),
        ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Inbt", 3)

    # --- She asks what exactly he likes about her tits/ass ---
    def chitchat_ask_what_about_tits(girl, loc, t_index):
        _is_small = getattr(girl, "bust", "medium") == "small"
        set_scene_expression(girl, "shy")
        Say_Line(girl, _("So... you said you like my breasts... but what exactly do you like about them?"))

        if _is_small:
            choices = [
                (_("I think they're the perfect size."), "size"),
                (_("I like thinking about using them in other ways."), "use"),
                (_("They suit you really well."), "sweet"),
            ]
        else:
            choices = [
                (_("I think it's incredible how big they are."), "size"),
                (_("I like thinking about using them in other ways."), "use"),
                (_("They suit you really well."), "sweet"),
            ]
        result = renpy.display_menu(choices)

        if result == "size":
            if _is_small:
                set_scene_expression(girl, "embarrassed", blush="1")
                Say_Line(girl, _("Perfect? You really think so? That... means a lot."))
                Change_Status(girl, "Love", 8)
                Change_Status(girl, "Inbt", 3)
            else:
                set_scene_expression(girl, "smile")
                Say_Line(girl, _("You really can not help yourself, can you?"))
                Change_Status(girl, "Inbt", 5)
                Change_Status(girl, "Obed", 3)
        elif result == "use":
            if _is_small and not girl_has_pose(girl, "titjob"):
                set_scene_expression(girl, "sad", eyes="eyes_side")
                Say_Line(girl, _("Other ways? I mean... I'm not sure mine could do much for that."))
                Change_Status(girl, "Inbt", 3)
            else:
                set_scene_expression(girl, "shy")
                Say_Line(girl, _("Other ways...? I... I think I know what you mean."))
                Change_Status(girl, "Inbt", 5)
                Change_Status(girl, "Obed", 8)
        elif result == "sweet":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("That is... actually really sweet. Thank you."))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 3)

        set_scene_expression(girl, "normal")
        girl.set_flag("asked_what_about_tits")

    def chitchat_ask_what_about_ass(girl, loc, t_index):
        set_scene_expression(girl, "shy")
        Say_Line(girl, _("So... you said you like my ass... but what exactly do you like about it?"))

        choices = [
            (_("I think it's incredible how big it is."), "size"),
            (_("I like thinking about using it in other ways."), "use"),
            (_("It suits you really well."), "sweet"),
        ]
        result = renpy.display_menu(choices)

        if result == "size":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("So it is all about size for you, huh?"))
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Obed", 3)
        elif result == "use":
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("Other ways...? You better not be thinking what I think you are thinking."))
            Change_Status(girl, "Inbt", 5)
            Change_Status(girl, "Obed", 8)
        elif result == "sweet":
            set_scene_expression(girl, "smile")
            Say_Line(girl, _("That is... actually really sweet. Thank you."))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 3)

        set_scene_expression(girl, "normal")
        girl.set_flag("asked_what_about_ass")

    # ---------- FINANCIAL / ECONOMY HINTS ----------

    def chitchat_poor_money_hints(girl, loc, t_index):
        set_scene_expression(girl, "sad")
        _lines = [
            _("I've been eating instant noodles all week. Campus food is so expensive..."),
            _("My scholarship barely covers rent. Sometimes I wonder if I should pick up a side job..."),
            _("I saw this cute top at the mall but... maybe next month."),
            _("I had to skip coffee today. Can't afford it until Friday."),
            _("My roommate got a new laptop and I'm still using this broken one from high school..."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("Sorry, I didn't mean to make it awkward. It's fine, really."),
            _("Anyway, it's not a big deal. I'll figure it out."),
            _("Don't worry about it. I always manage somehow."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))

    def chitchat_rich_money_hints(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("Daddy just got me a new car for my birthday. Want to see it later?"),
            _("I'm thinking of redecorating my room. The current furniture is so last season."),
            _("I ordered takeout from that fancy Italian place again. I can't help it, the campus food is terrible."),
            _("I just bought the cutest pair of shoes online. They should arrive tomorrow."),
            _("My family is going to Europe for break. I'm trying to convince them to add another week."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("What? Why are you looking at me like that?"),
            _("I'm not bragging. I'm just... sharing."),
            _("Don't judge me. A girl deserves nice things."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))

    def chitchat_wants_gift(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        _lines = [
            _("You know what would be sweet? If someone surprised me with something..."),
            _("I saw the cutest necklace at the shop the other day. Just saying..."),
            _("It's been a while since anyone gave me a nice gift. Hint, hint."),
            _("I love surprises. Especially the kind you can hold in your hands."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_lines)))
        set_scene_expression(girl, "normal")
        _follow = [
            _("I'm not being subtle, am I?"),
            _("What? A girl can dream."),
            _("Forget I said anything. Unless you were already thinking about it."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))
        Change_Status(girl, "Love", 1)

    def chitchat_post_financial_shame(girl, loc, t_index):
        _fin_times = getattr(girl, "_financial_times", 0)
        _fin_att = _financial_attitude_stage(girl)

        if _fin_att >= 3:
            _set_standing_arm(girl, 3)
            set_scene_expression(girl, "normal")
            _key = "chitchat_s3"
        elif _fin_att == 2:
            _set_standing_arm(girl, 3)
            set_scene_expression(girl, "normal")
            _key = "chitchat_s2"
        else:
            set_scene_expression(girl, "sad")
            if _fin_times == 1:
                _key = "chitchat_shame_1"
            elif _fin_times == 2:
                _key = "chitchat_shame_2"
            else:
                _key = "chitchat_shame_3"
        Say_Line(girl, _fin_line(girl, _key))
        _set_standing_arm(girl, 0)
        set_scene_expression(girl, "normal")

    def chitchat_partner_nerd_complaint(girl, loc, t_index):
        _npc = get_npc_partner_for(girl)
        if not _npc:
            return
        _npc_name = _npc.name
        set_scene_expression(girl, "angry")
        _lines = [
            _("Do you know what PNAME has been doing? Playing video games ALL DAY. %(Pp)s barely talks to me anymore."),
            _("I gave PNAME five minutes to finish %(poss)s game. That was two hours ago."),
            _("PNAME keeps showing me %(poss)s game scores like I'm supposed to care. I couldn't care less."),
            _("I swear, PNAME loves that console more than %(pp)s loves me. It's pathetic."),
            _("PNAME canceled our date to play some stupid game. I'm THIS close to throwing it out the window."),
        ]
        # translate FIRST, then the name: a line with the name already in it has no pair
        _line = _tl(renpy.random.choice(_lines)).replace("PNAME", _npc_name)
        Say_Line(girl, _format_partner_line(girl, _line))
        set_scene_expression(girl, "normal")
        _follow = [
            _("Sorry... I just needed to vent."),
            _("Ugh, forget it. Let's talk about something else."),
            _("...Maybe I should hide it."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_follow)))

    # ==========================================================
    # TOPIC REGISTRATION
    # ==========================================================

    # ── Early-game introductions (one-shot, high priority) ──
    # Only eligible in the first 3 chitchat interactions with the girl
    register_chitchat(
        "global",
        chitchat_first_introduction,
        condition=lambda g, loc, t: (
            not g.get_flag("introduced_to_player")
            and g.GetActionCount("chitchat") < 3
        ),
        weight=10,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_what_do_you_do,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("asked_campus_activity")
            and g.GetActionCount("chitchat") < 3
        ),
        weight=8,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_player_hobby,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("shared_hobby")
            and g.GetActionCount("chitchat") < 3
        ),
        weight=6,
    )
    register_chitchat(
        "global",
        chitchat_do_you_work_out,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("asked_workout")
        ),
        weight=5,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_have_a_girlfriend,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("asked_girlfriend")
            and getattr(g, "Love", 0) >= 30
        ),
        weight=6,
    )

    register_chitchat(
        "global",
        chitchat_talked_to_others,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("asked_talked_to_others")
            and getattr(g, "Love", 0) >= 20
            # Only ask if there's actually at least one OTHER girl to talk about,
            # otherwise the menu degenerates to just "Actually, only you."
            and any(_og.gid != g.gid and _og.get_flag("introduced_to_player") for _og in ALL_GIRLS)
        ),
        weight=6,
        student=True,
    )

    # ── Early-game bonding (one-shot, Love 30+) ──
    register_chitchat(
        "global",
        chitchat_first_impression,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("first_impression_chat")
            and getattr(g, "Love", 0) >= 30
        ),
        weight=5,
    )
    register_chitchat(
        "global",
        chitchat_eat_together,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and not g.get_flag("ate_together")
            and getattr(g, "Love", 0) >= 20
        ),
        weight=5,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_you_look_different,
        condition=lambda g, loc, t: (
            g.get_flag("introduced_to_player")
            and getattr(g, "Love", 0) >= 50
        ),
        weight=3,
    )

    # "What are you up to?" — context-aware answer based on location + time.
    # High weight so the most common chit-chat actually responds to the player
    # instead of a random monologue.
    register_chitchat("global", chitchat_whats_up,                weight=5)

    # Global topics: always in the pool (plus new ones)
    register_chitchat("global", chitchat_global_study_reminder,   weight=2, student=True)
    register_chitchat("global", chitchat_global_teacher_gossip,   weight=1, student=True)

    register_chitchat("global", chitchat_global_coffee,            weight=2)
    register_chitchat("global", chitchat_global_group_project,     weight=2, student=True)
    register_chitchat("global", chitchat_global_cafeteria_food,    weight=1, student=True)
    register_chitchat("global", chitchat_global_weekend_plans,     weight=2)
    register_chitchat("global", chitchat_global_phone_distraction, weight=1)
    register_chitchat("global", chitchat_global_late_to_class,     weight=1, student=True)
    register_chitchat("global", chitchat_global_library,           weight=1, student=True)
    register_chitchat("global", chitchat_global_party_aftermath,   weight=1, student=True)
    register_chitchat("global", chitchat_global_sleep_deprived,    weight=2, student=True)
    register_chitchat("global", chitchat_global_campus_rumors,     weight=1, student=True)
    register_chitchat("global", chitchat_global_mr_johnson,       weight=1, student=True)
    register_chitchat("global", chitchat_global_weird_messages,   weight=1)
    register_chitchat("global", chitchat_global_exam_week,       weight=1, student=True)
    register_chitchat("global", chitchat_global_apocryphal_story, weight=1, student=True)

    # Time-based global topic (example: t_index >= 3 = evening)
    register_chitchat(
        "global",
        chitchat_global_too_late_to_study,
        condition=lambda g, loc, t: t >= 3,
        weight=1,
        student=True,
    )

    # Intimacy: only available after certain acts
    register_chitchat(
        "global",
        chitchat_intimate_teasing,
        condition=lambda g, loc, t: (
            get_sex_count(g, "sex") > 0 or get_sex_count(g, "bj") > 0
        ),
        weight=1,
    )

    # Study readiness: always available
    register_chitchat("global", chitchat_study_readiness, weight=2, student=True)

    # Girl asks player about studying
    register_chitchat("global", chitchat_girl_asks_player_study, weight=2, student=True)

    # Ask player's favorite position: Love or Inbt >= 300, and she doesn't know yet
    register_chitchat(
        "global",
        chitchat_ask_player_fav,
        condition=lambda g, loc, t: (
            (getattr(g, "Love", 0) >= 300 or getattr(g, "Inbt", 0) >= 300)
            and not hasattr(g, "player_fav_position")
        ),
        weight=3,
    )

    # Shower history: girl walked in on player
    register_chitchat(
        "global",
        chitchat_girl_caught_player_shower,
        condition=lambda g, loc, t: g.HasSeen("girl_walked_in_shower"),
        weight=3,
    )

    # Shower history: player walked in on girl
    register_chitchat(
        "global",
        chitchat_player_caught_girl_shower,
        condition=lambda g, loc, t: g.HasSeen("player_walked_in_shower"),
        weight=3,
    )

    # Girl comments on player's size after seeing him nude
    register_chitchat(
        "global",
        chitchat_girl_comments_player_size,
        condition=lambda g, loc, t: g.HasSeen("girl_saw_penis"),
        weight=3,
    )

    # Shower history: showered together
    register_chitchat(
        "global",
        chitchat_showered_together,
        condition=lambda g, loc, t: g.HasSeen("showered_together"),
        weight=3,
    )

    # Gym topics
    register_chitchat("global", chitchat_global_gym_soreness,    weight=1, student=True)
    register_chitchat("global", chitchat_global_gym_motivation,  weight=2, student=True)
    register_chitchat("global", chitchat_global_gym_crowded,     weight=1, student=True)

    # Exam / A grade topics
    register_chitchat(
        "global",
        chitchat_global_exam_help,
        condition=lambda g, loc, t: is_achievement_unlocked("neeeerd"),
        weight=3,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_global_exam_together,
        condition=lambda g, loc, t: is_achievement_unlocked("neeeerd"),
        weight=3,
        student=True,
    )

    # Max energy / fitness topics
    register_chitchat(
        "global",
        chitchat_global_max_energy,
        condition=lambda g, loc, t: is_achievement_unlocked("max_fit"),
        weight=3,
        student=True,
    )

    # Pool topics
    register_chitchat("global", chitchat_global_pool_relaxing,   weight=2, student=True)
    register_chitchat("global", chitchat_global_pool_tan,        weight=1, student=True)
    register_chitchat("global", chitchat_global_pool_splash,     weight=1, student=True)

    # High lust commentary: Lust > 50
    register_chitchat(
        "global",
        chitchat_high_lust,
        condition=lambda g, loc, t: getattr(g, "Lust", 0) > 50,
        weight=4,
    )

    # Partner distracted by nerd gift
    register_chitchat(
        "global",
        chitchat_partner_nerd_complaint,
        condition=lambda g, loc, t: (
            g.has_npc_partner()
            and getattr(g, "_npc_partner_received_nerd_gift", False)
        ),
        weight=3,
    )

    # Frieren
    register_chitchat("frieren", chitchat_frieren_magic_books, weight=2)
    register_chitchat("frieren", chitchat_frieren_exam_logic,  weight=1)
    register_chitchat(
        "frieren",
        chitchat_frieren_awkward_after_sex,
        condition=lambda g, loc, t: get_sex_count(g, "sex") > 0,
        weight=1,
    )

    # Pool events — very high weight, almost always triggers when conditions match (every girl: it was Gwen only
    # until 2026-09-19, the flow is generic and each one has her bikini in her rear pose)
    register_chitchat("global", chitchat_pool_sunscreen, condition=_sunscreen_chitchat_ok, weight=50)
    _CHITCHAT_HAS_MENU.add(chitchat_pool_sunscreen)   # a menu + a pose change: never over the phone

    # Gwen
    register_chitchat("gwen", chitchat_gwen_training,     weight=2)
    register_chitchat("gwen", chitchat_gwen_gym_vs_study, weight=1)
    register_chitchat(
        "gwen",
        chitchat_gwen_sly_tease,
        condition=lambda g, loc, t: get_sex_count(g, "tj") > 0,
        weight=1,
    )

    # Discovery topics (one-shot: disappear after flag is set)
    register_chitchat(
        "global",
        chitchat_discover_boyfriend,
        condition=lambda g, loc, t: (
            getattr(g, "Love", 0) >= 100
            and not g.get_flag("discovered_relationship")
        ),
        weight=3,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_discover_virgin,
        condition=lambda g, loc, t: (
            max(getattr(g, "Love", 0), getattr(g, "Inbt", 0)) >= 250
            and not g.get_flag("discovered_virgin")
        ),
        weight=3,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_discover_fav_act,
        condition=lambda g, loc, t: (
            max(getattr(g, "Love", 0), getattr(g, "Inbt", 0)) >= 300
            and not g.get_flag("discovered_fav_act")
        ),
        weight=3,
    )
    # Favorite food/drink HINTS — only clues (higher chance so players catch
    # them); the real preference is confirmed during events, not here. They keep
    # dropping until the preference is confirmed (discovered_fav_* set at event).
    register_chitchat(
        "global",
        chitchat_hint_fav_drink,
        condition=lambda g, loc, t: (
            max(getattr(g, "Love", 0), getattr(g, "Inbt", 0)) >= 200
            and not g.get_flag("discovered_fav_drink")
        ),
        weight=7,
    )
    register_chitchat(
        "global",
        chitchat_hint_fav_food,
        condition=lambda g, loc, t: (
            max(getattr(g, "Love", 0), getattr(g, "Inbt", 0)) >= 200
            and not g.get_flag("discovered_fav_dish")
        ),
        weight=7,
    )

    # Trait-hint topics (global)
    register_chitchat(
        "global",
        chitchat_hint_cameras,
        condition=lambda g, loc, t: getattr(g, "Love", 0) >= 150,
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_hint_protection,
        condition=lambda g, loc, t: getattr(g, "Inbt", 0) >= 200,
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_hint_public_thrill,
        condition=lambda g, loc, t: getattr(g, "Love", 0) >= 200,
        weight=2,
        student=True,
    )
    register_chitchat(
        "global",
        chitchat_hint_intensity,
        condition=lambda g, loc, t: (
            getattr(g, "Inbt", 0) >= 250
            and get_sex_count(g, "sex") > 0
        ),
        weight=2,
    )

    # --- Anal preference hint (discovery) ---
    register_chitchat(
        "global",
        chitchat_hint_anal,
        condition=lambda g, loc, t: (
            getattr(g, "Inbt", 0) >= 300
            and (get_sex_count(g, "sex") > 0 or get_sex_count(g, "anal") > 0)
        ),
        weight=2,
    )

    # --- Anal reflection (post-anal, requires trait) ---
    register_chitchat(
        "global",
        chitchat_anal_reflection,
        condition=lambda g, loc, t: (
            get_sex_count(g, "anal") > 0
            and (g.has_trait("anal_lover") or g.has_trait("anal_hater"))
        ),
        weight=3,
    )

    # --- Anal hater confrontation (hater-exclusive, after being forced) ---
    register_chitchat(
        "global",
        chitchat_anal_hater_confrontation,
        condition=lambda g, loc, t: (
            g.has_trait("anal_hater")
            and get_sex_count(g, "anal") > 0
        ),
        weight=4,
    )

    # --- History-based topics (require specific experiences) ---

    # After first penetrative sex
    register_chitchat(
        "global",
        chitchat_history_first_sex,
        condition=lambda g, loc, t: get_sex_count(g, "sex") > 0,
        weight=3,
    )

    # After BJ experience
    register_chitchat(
        "global",
        chitchat_history_bj,
        condition=lambda g, loc, t: get_sex_count(g, "bj") > 0,
        weight=2,
    )

    # After HJ experience
    register_chitchat(
        "global",
        chitchat_history_hj,
        condition=lambda g, loc, t: get_sex_count(g, "hj") > 0,
        weight=2,
    )

    # After TJ experience
    register_chitchat(
        "global",
        chitchat_history_tj,
        condition=lambda g, loc, t: get_sex_count(g, "tj") > 0,
        weight=2,
    )

    # After creampie
    register_chitchat(
        "global",
        chitchat_history_creampie,
        condition=lambda g, loc, t: getattr(g, "CreampieCounts", 0) > 0,
        weight=3,
    )

    # After being filmed (check if any video of this girl exists)
    register_chitchat(
        "global",
        chitchat_history_filmed,
        condition=lambda g, loc, t: any(
            v.get("girl_gid") == g.gid and v.get("consensual", True)
            for v in getattr(store.Player, "recorded_videos", [])
        ),
        weight=3,
    )

    # After raw sex (no condom)
    register_chitchat(
        "global",
        chitchat_history_raw_sex,
        condition=lambda g, loc, t: getattr(g, "raw_sex_count", 0) > 0,
        weight=2,
    )

    # After multiple orgasms (at least 3 total)
    register_chitchat(
        "global",
        chitchat_history_orgasm,
        condition=lambda g, loc, t: sum(getattr(g, "Orgasms", {}).values()) >= 3,
        weight=2,
    )

    # BF-aware: after cheating acts (girl has bf and has cheated)
    register_chitchat(
        "global",
        chitchat_history_cheating,
        condition=lambda g, loc, t: (
            hasattr(g, "has_npc_partner") and g.has_npc_partner()
            and sum(getattr(g, "CheatActs", {}).values()) > 0
        ),
        weight=3,
    )

    # --- Witness history topics ---

    # She was cheated on (witnessed player with another girl while dating him)
    register_chitchat(
        "global",
        chitchat_witness_cheated_on,
        condition=lambda g, loc, t: _has_witness_type(g, "witness_was_cheated_on"),
        weight=4,
    )

    # She saw another girl cheating on her BF with the player
    register_chitchat(
        "global",
        chitchat_witness_saw_girl_cheat,
        condition=lambda g, loc, t: _has_witness_type(g, "witness_saw_girl_cheat"),
        weight=3,
    )

    # She saw both cheating (player cheating on her + the girl cheating on her BF)
    register_chitchat(
        "global",
        chitchat_witness_saw_both_cheat,
        condition=lambda g, loc, t: _has_witness_type(g, "witness_saw_both_cheat"),
        weight=4,
    )

    # She saw acts in public
    register_chitchat(
        "global",
        chitchat_witness_public,
        condition=lambda g, loc, t: _has_witness_public(g),
        weight=3,
    )

    # Location-specific: pool
    register_chitchat(
        "global",
        chitchat_witness_pool,
        condition=lambda g, loc, t: _has_witness_location(g, "pool"),
        weight=3,
    )

    # Location-specific: shower
    register_chitchat(
        "global",
        chitchat_witness_shower,
        condition=lambda g, loc, t: (
            _has_witness_location(g, "shower")
            or _has_witness_location(g, "showers")
        ),
        weight=3,
    )

    # Location-specific: bedroom/room
    register_chitchat(
        "global",
        chitchat_witness_bedroom,
        condition=lambda g, loc, t: (
            _has_witness_location(g, "room")
            or _has_witness_location(g, "bedroom")
        ),
        weight=2,
    )

    # She stayed and watched
    register_chitchat(
        "global",
        chitchat_witness_watched,
        condition=lambda g, loc, t: _has_witness_act(g, "watched"),
        weight=3,
    )

    # She joined the session
    register_chitchat(
        "global",
        chitchat_witness_joined,
        condition=lambda g, loc, t: _has_witness_act(g, "joined"),
        weight=3,
    )

    # She left embarrassed
    register_chitchat(
        "global",
        chitchat_witness_embarrassed,
        condition=lambda g, loc, t: (
            _has_witness_act(g, "left_embarrassed")
            or _has_witness_act(g, "left_embarrassed_midact")
        ),
        weight=3,
    )

    # --- Player-GF cheating progression topics ---

    # First time helping player cheat on his GF
    register_chitchat(
        "global",
        chitchat_pgf_cheat_first,
        condition=lambda g, loc, t: (
            int(getattr(g, "PlayerCheatCount", 0)) >= 1
            and int(getattr(g, "PlayerCheatCount", 0)) <= 1
            and player_has_girlfriend(ALL_GIRLS)
            and not g.is_dating_player()
            and not is_player_harem_exempt(g)
        ),
        weight=5,
    )

    # Recurring cheating (2-4 times)
    register_chitchat(
        "global",
        chitchat_pgf_cheat_recurring,
        condition=lambda g, loc, t: (
            int(getattr(g, "PlayerCheatCount", 0)) >= 2
            and int(getattr(g, "PlayerCheatCount", 0)) <= 4
            and player_has_girlfriend(ALL_GIRLS)
            and not g.is_dating_player()
            and not is_player_harem_exempt(g)
        ),
        weight=4,
    )

    # Veteran cheating (5+ times)
    register_chitchat(
        "global",
        chitchat_pgf_cheat_veteran,
        condition=lambda g, loc, t: (
            int(getattr(g, "PlayerCheatCount", 0)) >= 5
            and player_has_girlfriend(ALL_GIRLS)
            and not g.is_dating_player()
            and not is_player_harem_exempt(g)
        ),
        weight=4,
    )

    # --- Relationship-aware topics ---

    # Dating the player
    register_chitchat(
        "global",
        chitchat_dating_couple_talk,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "dating",
        weight=3,
    )
    register_chitchat(
        "global",
        chitchat_dating_jealousy,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "dating" and not g.has_trait("polyamorous"),
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_dating_future_plans,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "dating",
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_dating_pet_names,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "dating",
        weight=2,
    )

    # Ex-girlfriend
    register_chitchat(
        "global",
        chitchat_ex_awkward,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "ex",
        weight=3,
    )
    register_chitchat(
        "global",
        chitchat_ex_regret,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "ex",
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_ex_moving_on,
        condition=lambda g, loc, t: getattr(g, "Player_status", "none") == "ex",
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_ex_second_chances,
        condition=lambda g, loc, t: (
            getattr(g, "Player_status", "none") == "ex"
            and getattr(g, "Love", 0) >= 300
        ),
        weight=3,
    )

    # Has NPC boyfriend (not dating player)
    register_chitchat(
        "global",
        chitchat_npc_bf_sweet,
        condition=lambda g, loc, t: (
            hasattr(g, "has_npc_partner") and g.has_npc_partner()
            and getattr(g, "Player_status", "none") != "dating"
        ),
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_npc_bf_advice,
        condition=lambda g, loc, t: (
            hasattr(g, "has_npc_partner") and g.has_npc_partner()
            and getattr(g, "Player_status", "none") != "dating"
        ),
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_npc_bf_doubts,
        condition=lambda g, loc, t: (
            hasattr(g, "has_npc_partner") and g.has_npc_partner()
            and getattr(g, "Player_status", "none") != "dating"
            and getattr(g, "Love", 0) >= 200
        ),
        weight=3,
    )
    register_chitchat(
        "global",
        chitchat_npc_bf_comparing,
        condition=lambda g, loc, t: (
            hasattr(g, "has_npc_partner") and g.has_npc_partner()
            and getattr(g, "Player_status", "none") != "dating"
            and getattr(g, "Love", 0) >= 300
        ),
        weight=3,
    )

    # --- Financial coercion topics ---

    # Poor girl hints about money struggles
    register_chitchat(
        "global",
        chitchat_poor_money_hints,
        condition=lambda g, loc, t: g.has_trait("poor"),
        weight=2,
        student=True,
    )
    # Rich girl shows off wealth
    register_chitchat(
        "global",
        chitchat_rich_money_hints,
        condition=lambda g, loc, t: g.has_trait("rich"),
        weight=1,
        student=True,
    )
    # Girl subtly wants a gift
    register_chitchat(
        "global",
        chitchat_wants_gift,
        condition=lambda g, loc, t: (
            getattr(g, "Love", 0) >= 200
            and g.GetActionCount("gift_given") < 3
        ),
        weight=1,
    )
    # Post-financial shame
    register_chitchat(
        "global",
        chitchat_post_financial_shame,
        condition=lambda g, loc, t: getattr(g, "_financial_times", 0) > 0,
        weight=2,
    )

    # High love but not dating (Love >= 700)
    register_chitchat(
        "global",
        chitchat_high_love_hints,
        condition=lambda g, loc, t: (
            getattr(g, "Love", 0) >= 700
            and getattr(g, "Player_status", "none") not in ("dating", "exclusive")
        ),
        weight=3,
    )
    register_chitchat(
        "global",
        chitchat_high_love_frustration,
        condition=lambda g, loc, t: (
            getattr(g, "Love", 0) >= 700
            and getattr(g, "Player_status", "none") not in ("dating", "exclusive")
        ),
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_high_love_flirty,
        condition=lambda g, loc, t: (
            getattr(g, "Love", 0) >= 700
            and getattr(g, "Player_status", "none") not in ("dating", "exclusive")
        ),
        weight=3,
    )

    # Low love (Love < 300)
    register_chitchat(
        "global",
        chitchat_low_love_cold,
        condition=lambda g, loc, t: getattr(g, "Love", 0) < 300,
        weight=2,
    )
    register_chitchat(
        "global",
        chitchat_low_love_distant,
        condition=lambda g, loc, t: getattr(g, "Love", 0) < 300,
        weight=2,
    )

    # ==========================================================
    # BF LOYALTY CHITCHAT — hints about her relationship status
    # ==========================================================

    # --- In Love (750-1000): she talks positively about her BF ---
    def chitchat_bf_in_love(girl, loc, t_index):
        _discover_partner(girl)
        set_scene_expression(girl, "smile")
        _lines = [
            _("My %(pl)s texted me this morning. %(Pp)s's so sweet sometimes."),
            _("I'm seeing my %(pl)s later. %(Pp)s planned something nice for us."),
            _("%(Pp)s surprised me with my favorite snack yesterday. Little things, you know?"),
            _("I was thinking about my %(pl)s... {hint}I really like %(po)s a lot.{/hint}"),
            _("My %(pl)s makes me feel safe. That's important to me."),
        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_lines))))
        set_scene_expression(girl, "happy")
        _follow = [
            _("{hint}I'm really happy in my relationship right now.{/hint}"),

            _("I hope it stays like this forever."),
            _("%(Pp)s's great. I'm lucky."),
            _("Sorry if I talk about %(po)s too much. I just... really like %(po)s."),
        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_follow))))

    # --- Normal (500-750): she likes him but it's routine ---
    def chitchat_bf_normal(girl, loc, t_index):
        _discover_partner(girl)
        set_scene_expression(girl, "normal")
        _lines = [
            _("My %(pl)s? Yeah, %(pp)s's fine. Nothing exciting, but %(pp)s's fine."),
            _("We haven't done anything fun in a while. %(Pp)s's kind of predictable."),
            _("%(Pp)s's nice. {hint}Just... nice. You know?{/hint}"),
            _("My %(pl)s and I had dinner yesterday. It was okay, I guess."),
            _("%(Pp)s's sweet, but sometimes I wonder if there's more out there..."),
        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_lines))))
        set_scene_expression(girl, "normal")
        _follow = [
            _("{hint}I like %(po)s, but I'm not head over heels or anything.{/hint}"),

            _("Is it bad that I don't miss %(po)s when %(pp)s's not around?"),
            _("%(Pp)s's comfortable. Like an old sweater. That's not bad, right?"),
            _("Anyway... enough about %(po)s. What about you?"),
        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_follow))))

    # --- Strained (250-500): she's losing interest ---
    def chitchat_bf_strained(girl, loc, t_index):
        _discover_partner(girl)
        set_scene_expression(girl, "sad")
        _lines = [
            _("My %(pl)s forgot my... never mind. It doesn't matter."),
            _("%(Pp)s never wants to do anything fun. {hint}I'm getting bored.{/hint}"),
            _("We argued again last night. Over something stupid. As usual."),
            _("Sometimes I wonder why I'm even with %(po)s, honestly."),
            _("%(Pp)s barely texts me anymore. {hint}Not that I really care...{/hint}"),
        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_lines))))
        set_scene_expression(girl, "normal")
        _follow = [
            _("{hint}I don't think I like %(po)s as much as I used to.{/hint}"),

            _("Maybe I'm being unfair. But I can't help how I feel."),
            _("Talking to you is more fun than talking to %(po)s, honestly."),
            _("Sorry, I didn't mean to dump all that on you."),
            _("{hint}I feel like I'm staying out of habit, not love.{/hint}"),

        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_follow))))

    # --- Miserable (0-250): she's done with him ---
    def chitchat_bf_miserable(girl, loc, t_index):
        _discover_partner(girl)
        set_scene_expression(girl, "angry")
        _lines = [
            _("My %(pl)s is SO boring. I can't stand it anymore."),
            _("%(Pp)s does NOTHING for me. {hint}I don't even know why I'm still with %(po)s.{/hint}"),
            _("I dread seeing %(po)s. Is that terrible? Because I don't care."),
            _("%(Pp)s called me today and I just... didn't pick up."),
            _("Every conversation with %(po)s is the same. I'm losing my mind."),
        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_lines))))
        set_scene_expression(girl, "sad")
        _follow = [
            _("{hint}Honestly? I think %(pp)s bores me to death.{/hint} Someone needs to rescue me."),

            _("You're way more interesting than %(pp)s is. Just saying."),
            _("{hint}I'm this close to breaking up with %(po)s.{/hint} Don't tell anyone."),

            _("I need someone who actually makes me feel something. %(Pp)s doesn't."),
            _("{hint}I'd rather spend time with you than with %(po)s.{/hint} That says a lot."),

        ]
        Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_follow))))

    # --- Condition helpers ---
    def _has_bf_loyalty_tier(girl, tier):
        if not hasattr(girl, "has_npc_partner") or not girl.has_npc_partner():
            return False
        return hasattr(girl, "bf_loyalty_tier") and girl.bf_loyalty_tier() == tier

    # --- Register BF chitchat topics ---
    register_chitchat(
        "global",
        chitchat_bf_in_love,
        condition=lambda g, loc, t: _has_bf_loyalty_tier(g, "in_love"),
        weight=3,
    )
    register_chitchat(
        "global",
        chitchat_bf_normal,
        condition=lambda g, loc, t: _has_bf_loyalty_tier(g, "normal"),
        weight=3,
    )
    register_chitchat(
        "global",
        chitchat_bf_strained,
        condition=lambda g, loc, t: _has_bf_loyalty_tier(g, "strained"),
        weight=4,
    )
    register_chitchat(
        "global",
        chitchat_bf_miserable,
        condition=lambda g, loc, t: _has_bf_loyalty_tier(g, "miserable"),
        weight=5,
    )

    # Compliment body awareness: she knows he keeps thinking about her tits
    register_chitchat(
        "global",
        chitchat_knows_thinking_tits,
        condition=lambda g, loc, t: g.GetActionCount("complimented_tits") >= 1,
        weight=2,
    )
    # Compliment body awareness: she knows he keeps thinking about her ass
    register_chitchat(
        "global",
        chitchat_knows_thinking_ass,
        condition=lambda g, loc, t: g.GetActionCount("complimented_ass") >= 1,
        weight=2,
    )
    # She asks what exactly he likes about her tits (one-shot)
    register_chitchat(
        "global",
        chitchat_ask_what_about_tits,
        condition=lambda g, loc, t: (
            g.GetActionCount("complimented_tits") >= 1
            and not g.get_flag("asked_what_about_tits")
        ),
        weight=4,
    )
    # She asks what exactly he likes about her ass (one-shot)
    register_chitchat(
        "global",
        chitchat_ask_what_about_ass,
        condition=lambda g, loc, t: (
            g.GetActionCount("complimented_ass") >= 1
            and not g.get_flag("asked_what_about_ass")
        ),
        weight=4,
    )

    # ==========================================================
    # ESCALATION MEMORY CHITCHATS
    # Girl remembers escalation events (rub->tip, tip->sex)
    # ==========================================================

    def chitchat_escalation_rub_to_tip(girl, loc, t_index):
        _is_hc = girl.has_trait("hardcore_sex")
        _is_cute = girl.has_trait("cute_sex")
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

        if _has_bf:
            lines = [
                _format_partner_line(girl, _("Remember when I asked you to put the tip in? I still can't believe I did that... my %(pl)s would kill me if %(pp)s knew.")),
                _format_partner_line(girl, _("That time I begged for 'just the tip'... I think about it more than I should. Especially when I'm with %(po)s.")),
                _("I told myself it was just rubbing. Then I wanted the tip. What's wrong with me?"),
            ]
        elif _is_hc:
            lines = [
                _("Remember when I told you to put the tip in? I knew exactly what I was doing."),
                _("That escalated fast, didn't it? From rubbing to the tip... I regret nothing."),
                _("I asked for the tip because I knew I'd want more. And I was right."),
            ]
        elif _is_cute:
            lines = [
                _("I... I still think about when I asked you to put the tip in. I can't believe I said that out loud..."),
                _("Remember when we were just rubbing and I... asked for more? I was so embarrassed..."),
                _("I told myself 'just rubbing' and then I begged for the tip. What happened to me?"),
            ]
        else:
            lines = [
                _("Remember when I asked you to put the tip in? I couldn't help myself."),
                _("We went from rubbing to the tip pretty fast that time, didn't we?"),
                _("I still think about when I gave in and asked for the tip. No regrets."),
            ]

        set_scene_expression(girl, "shy")
        Say_Line(girl, renpy.random.choice(lines))

    register_chitchat(
        "global",
        chitchat_escalation_rub_to_tip,
        condition=lambda g, loc, t: g.flags.get("escalated_rub_to_tip", False),
        weight=3,
    )

    def chitchat_escalation_tip_to_sex(girl, loc, t_index):
        _is_hc = girl.has_trait("hardcore_sex")
        _is_cute = girl.has_trait("cute_sex")
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _was_virgin = girl.flags.get("escalated_lost_virginity", False)

        if _was_virgin:
            lines = [
                _("I lost my virginity because I couldn't stop at 'just the tip'. I don't know how to feel about that."),
                _("My first time was because I begged you to go deeper. Not exactly how I imagined it..."),
                _("I went from 'just rubbing' to losing my virginity in the same session. That's... something."),
                _("I always thought my first time would be romantic. Instead I begged for it during 'just the tip'..."),
            ]
        elif _has_bf:
            lines = [
                _tl(_("I let you go all the way when I said 'just the tip'. My %s has no idea how far I've fallen.")) % girl.partner_label(),
                _("From tip to full sex... and I was the one who asked for it. I'm a terrible girlfriend."),
                _tl(_("Remember when I said 'forget the tip, go all the way'? I think about that every time I see my %s.")) % girl.partner_label(),
                _("I cheated because I couldn't stop at the tip. And the worst part? I'd do it again."),
            ]
        # steering him without him knowing is femdom, not hardcore (docs/plan_femdom.md D3)
        elif girl.has_trait("femdom"):
            lines = [
                _("That escalation from tip to sex? I planned that. You just didn't know it yet."),
                _("From the tip to all the way in... and I decided when. Remember that."),
                _("You think you got further than the tip? I let you. There's a difference."),
            ]
        elif _is_hc:
            lines = [
                _("Remember when I told you to forget the tip and just fuck me? Best decision I ever made."),
                _("From the tip to all the way in. I knew that's where it was going. I wanted it."),
            ]
        elif _is_cute:
            lines = [
                _("I still can't believe I begged you to go deeper that time... I was so caught up in the moment..."),
                _("From 'just the tip' to... everything. I never thought I'd be that kind of girl."),
                _("I think about that time a lot. When I couldn't stop at the tip. It was so intense..."),
            ]
        else:
            lines = [
                _("Remember when we went from 'just the tip' to full on sex? I fell for the oldest trick in the book."),
                _("I said 'just the tip' and then begged for more. Classic, right?"),
                _("That escalation from tip to sex... I knew it was coming. I just didn't want to admit it."),
            ]

        set_scene_expression(girl, "shy")
        Say_Line(girl, renpy.random.choice(lines))

    register_chitchat(
        "global",
        chitchat_escalation_tip_to_sex,
        condition=lambda g, loc, t: g.flags.get("escalated_tip_to_sex", False),
        weight=4,
    )

    def chitchat_escalation_cheated_bf(girl, loc, t_index):
        lines = [
            _format_partner_line(girl, _("I cheated on %(po)s because of you. Because I couldn't control myself. Are you happy?")),
            _format_partner_line(girl, _("%(Pp)s trusts me completely. And I let you inside me because I couldn't stop at the tip. What kind of person am I?")),
            _tl(_("Every time I see my %s I think about what we did. How I begged you for more.")) % girl.partner_label(),
            _("I keep telling myself it was a mistake. But then I remember how it felt and I want to do it again."),
        ]
        set_scene_expression(girl, "sad")
        Say_Line(girl, renpy.random.choice(lines))

    register_chitchat(
        "global",
        chitchat_escalation_cheated_bf,
        condition=lambda g, loc, t: g.flags.get("escalated_cheated_bf", False),
        weight=5,
    )

    # ── Ex-cheating resolved: post-breakup chit-chats ──────────

    def chitchat_ex_cheating_awkward(girl, loc, t_index):
        """Post-breakup awkwardness. She's trying to act normal but can't."""
        _is_cute = girl.has_trait("cute_sex")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_loyal = girl.has_trait("loyal")
        _is_cheater = girl.has_trait("cheater")

        if _is_cute:
            set_scene_expression(girl, "shy", blush=1)
            Say_Line(girl, renpy.random.choice([
                _("This is weird, isn't it? Talking to you like nothing happened. I keep wanting to cry and I don't even know why anymore."),
                _("I practiced what I was going to say to you in the mirror this morning. And now I can't remember a single word."),
                _("I keep catching myself staring at you and then looking away. Old habits, I guess. Sorry. I don't mean to make it weird."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("...I miss how easy things used to be between us. Before everything got complicated."),
                _("...Do you think we'll ever be able to talk without this... heaviness?"),
                _("...I wonder if laughing with you will ever feel normal again."),
            ]))
        elif _is_hc:
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("So... are we going to keep doing this thing where we pretend everything is fine? Because I'm over it."),
                _("Look, this whole 'polite small talk' act is killing me. Can we just acknowledge the elephant in the room and move on?"),
                _("I'd rather we be real with each other than play this stupid game of 'everything is normal.' It's not. We both know it."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...Whatever. At least we're talking. That's more than I expected, honestly."),
                _("...I'm not going to pretend I'm over it. But I'm here. So that's something."),
                _("...Just don't bore me with small talk. If we're going to talk, let's actually TALK."),
            ]))
        elif _is_loyal:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("You know what's funny? I still instinctively save a seat for you at lunch. And then I remember we're not... that anymore."),
                _("I found one of your things in my room the other day. I held it for like ten minutes before putting it away. Pathetic, right?"),
                _("Sometimes I forget for a second. And then I remember what you did and it hits me all over again. Like a punch to the stomach."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...Sorry. I didn't mean to make this heavy. I'm just... adjusting."),
                _("...Ignore me. I'm being dramatic. We said we'd move on. So let's move on."),
                _("...I promised myself I wouldn't bring it up again. But it's hard when every conversation feels like walking on glass."),
            ]))
        elif _is_cheater:
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("You know, for two people who messed everything up, we're doing surprisingly okay as friends."),
                _("It's actually kind of nice not having to pretend anymore. No rules, no expectations. Just... this."),
                _("Funny how things work out. We were terrible at dating. But this? This might actually work."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...Don't read too much into that. I'm just saying it's less stressful."),
                _("...I mean, the sex was great. But the drama? Not worth it. This is better."),
                _("...Who knows. Maybe we needed to crash and burn to figure out what actually works between us."),
            ]))
        else:
            set_scene_expression(girl, "normal", eyes="eyes_side")
            Say_Line(girl, renpy.random.choice([
                _("I keep starting conversations in my head with you. Full dialogues. And then when I actually see you I just say 'hey.'"),
                _("Is it just me or do our silences feel louder now? Like every pause is loaded with all the things we're not saying."),
                _("I ran into you at the hallway yesterday and my heart did that stupid thing where it speeds up. I hate that it still does that."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("...Anyway. I'm glad we can at least talk. Even if it's about nothing."),
                _("...I guess this is our new normal. It's not great. But it's not terrible."),
                _("...One day at a time, right?"),
            ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)

    def chitchat_ex_cheating_trust(girl, loc, t_index):
        """She reflects on trust and what was lost."""
        _is_cute = girl.has_trait("cute_sex")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_loyal = girl.has_trait("loyal")
        _is_cheater = girl.has_trait("cheater")

        if _is_cute:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I used to tell you everything. Like, EVERYTHING. Even the embarrassing stuff. I don't know who to tell those things to now."),
                _("My friends keep asking me if I'm okay. And I say yes. But I'm lying. I don't want to explain it because then I'd have to relive it."),
                _("I had a dream about you last night. We were still together and nothing bad happened. Waking up was the worst part."),
            ]))
            set_scene_expression(girl, "shy", blush=1)
            Say_Line(girl, renpy.random.choice([
                _("...Sorry for dumping this on you. You're probably the last person I should be telling."),
                _("...I know I shouldn't say this stuff to you. But who else would understand?"),
            ]))
        elif _is_hc:
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([
                _("You know what pisses me off the most? It's not that you did it. It's that I didn't see it coming. I'm usually smarter than that."),
                _("I keep going over it in my head. Trying to figure out when I lost control of the situation. And I can't pinpoint it. That drives me insane."),
                _("People think I'm over it because I'm not crying about it. But that's not how I work. My anger is quiet. And it lasts."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("...But holding grudges is exhausting. And I have better things to do with my energy."),
                _("...At least I learned something. Trust has to be earned. Not given. I won't make that mistake again."),
            ]))
        elif _is_loyal:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I keep asking myself if there were signs I missed. If I was too trusting. Too blind. Too in love to see what was happening."),
                _("The worst part isn't the betrayal. It's the doubt. Now I question everything. Every conversation, every memory. Was any of it real?"),
                _("I gave you my trust like it was nothing. Because to me, it WAS nothing. It was automatic. Now I realize how expensive that was."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...I'll trust again someday. But never the same way I trusted you. That version of me is gone."),
                _("...I don't say this to hurt you. I say it because you should know what you broke."),
            ]))
        elif _is_cheater:
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("Trust? Please. Neither of us was built for that. We just pretended long enough to believe our own lie."),
                _("Honestly? The whole 'exclusive' thing was always going to end this way. People like us aren't wired for monogamy."),
                _("I'm not even mad about the trust thing. I'm mad we wasted time pretending we were something we're not."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...At least now there's no illusion to maintain. That's freeing, in a weird way."),
                _("...We're better off being honest about what we want. Even if what we want is messy."),
            ]))
        else:
            set_scene_expression(girl, "sad", eyes="eyes_side")
            Say_Line(girl, renpy.random.choice([
                _("You know what I think about sometimes? How I used to fall asleep feeling safe because I knew you were mine. That feeling is gone now."),
                _("I trusted you with the ugly parts of me. The insecurities, the fears, the stuff I never show anyone. And then you went and proved them all right."),
                _("It's not just that you cheated. It's that you made me feel stupid for believing you wouldn't. THAT'S what stings."),
            ]))
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("...But life goes on. And honestly? I'm stronger now. Even if the strength came from a shitty place."),
                _("...I don't need you to fix it. I just needed you to hear it. That's enough."),
            ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 5)

    def chitchat_ex_cheating_memories(girl, loc, t_index):
        """She brings up a specific memory from when they were together."""
        _is_cute = girl.has_trait("cute_sex")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_loyal = girl.has_trait("loyal")
        _is_cheater = girl.has_trait("cheater")

        if _is_cute:
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("Remember when we first started talking and I was so nervous I couldn't even make eye contact? God, that feels like a lifetime ago."),
                _("I was organizing my photos and found the ones from when we were together. I stared at them way longer than I should have."),
                _("You know what I miss? The stupid stuff. Like how you'd make fun of my sneezes. Nobody does that anymore. It's dumb, but I miss it."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("...Sorry. I shouldn't bring up the good times. It makes the bad part hurt worse."),
                _("...Ugh, why did I say that. Now I'm getting emotional again. Ignore me."),
                _("...And now I'm sad. Great. This is why I shouldn't talk to you about feelings."),
            ]))
        elif _is_hc:
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I was cleaning my room and found that thing you left behind. Almost threw it out. ...Almost."),
                _("Someone mentioned your name the other day and I had this whole internal debate about whether I still care. The fact that I debated it at all is annoying."),
                _("You know what I think about sometimes? How confident I was that we'd work. How sure I was. I'm never that sure about anything anymore."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...Don't get sentimental on me. I'm not going soft. I'm just... observing."),
                _("...That came out more emotional than I intended. Pretend I said something tough instead."),
                _("...Anyway. Past is past. But it was a good past. Before it wasn't."),
            ]))
        elif _is_loyal:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("I wrote you a letter once. Before everything fell apart. I was going to give it to you on our anniversary. I burned it last week."),
                _("Remember when you told me I was the most important person in your life? I believed that so completely. I built my entire world around those words."),
                _("There are songs I can't listen to anymore. Places I can't go without thinking of you. You're everywhere and nowhere at the same time."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...I'll stop living in the past eventually. But for now, the memories are all I have left of who I used to be with you."),
                _("...Don't worry. I'm not trying to guilt you. I'm just... processing. Out loud. Sorry."),
            ]))
        elif _is_cheater:
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([
                _("You know what I actually miss? The sneaking around. The thrill of it. The relationship part was whatever, but the GAME? That was fun."),
                _("Honestly the best part of us dating was the sex. The emotional stuff was just... packaging. At least now we can skip the wrapping paper."),
                _("Remember when we tried to be 'serious'? Like, actually committed? That lasted what, a month before one of us got bored? Classic us."),
            ]))
            Say_Line(girl, renpy.random.choice([
                _("...Don't take that the wrong way. I enjoyed it. I just enjoy THIS more. Less pretending."),
                _("...We had fun. We'll have fun again. Just... differently. And honestly, probably better."),
            ]))
        else:
            set_scene_expression(girl, "normal")
            Say_Line(girl, renpy.random.choice([
                _("I was thinking about the first time you made me laugh. Like, REALLY laugh. The kind where your stomach hurts. I haven't laughed like that since."),
                _("There's a coffee shop we used to go to together. I went back yesterday. Sat in the same spot. Ordered the same thing. It tasted different."),
                _("Isn't it weird how you can know everything about someone and then suddenly not know them at all? Like they're a stranger wearing a familiar face."),
            ]))
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([
                _("...I don't know why I'm telling you this. Maybe because you're the only one who'd understand."),
                _("...Sometimes I think the memories are harder than the actual breakup. Because they prove it was real."),
                _("...Anyway. Enough nostalgia. Let's talk about something that doesn't make me want to eat ice cream alone at 2am."),
            ]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 5)

    register_chitchat(
        "global",
        chitchat_ex_cheating_awkward,
        condition=lambda g, loc, t: getattr(g, "_cheating_ex_resolved", False),
        weight=5,
    )
    register_chitchat(
        "global",
        chitchat_ex_cheating_trust,
        condition=lambda g, loc, t: getattr(g, "_cheating_ex_resolved", False),
        weight=4,
    )
    register_chitchat(
        "global",
        chitchat_ex_cheating_memories,
        condition=lambda g, loc, t: getattr(g, "_cheating_ex_resolved", False),
        weight=3,
    )

    # ── Ex trust milestones (both normal and cheating exes) ──

    def chitchat_ex_trust_halfway(girl, loc, t_index):
        if getattr(girl, "_cheating_ex_reconciled", False):
            if girl.has_trait("loyal"):
                _pool = [
                    _("I've been watching you. Really watching. And... you haven't given me a reason to doubt you. Not once. That means something."),
                    _("I keep waiting for the other shoe to drop. But it hasn't. Maybe... maybe you really have changed."),
                ]
            elif girl.has_trait("hardcore_sex"):
                _pool = [
                    _("I'll give you credit. You've been on your best behavior. I'm still watching, though. Don't get cocky."),
                    _("Alright. I'll admit it. You've surprised me. I didn't think you'd actually stick around and behave."),
                ]
            elif girl.has_trait("cute_sex"):
                _pool = [
                    _("Hey... I just wanted to say... I've noticed how hard you're trying. It makes me feel... safer. Thank you."),
                    _("I had a dream last night where everything was normal between us. No worries, no doubt. I woke up and realized... maybe we're getting there."),
                ]
            else:
                _pool = [
                    _("You know, I've been less paranoid lately. I used to check your phone in my head constantly. Now I just... don't. Progress, right?"),
                    _("I think I'm starting to relax around you again. Not all the way, but... more than before. That feels good."),
                ]
        else:
            _pool = [
                _("Things feel different this time around. Better. Like we actually learned from what happened."),
                _("I was scared to try this again, but... I'm glad I did. You've been really good to me."),
            ]
        set_scene_expression(girl, "worried")
        Say_Line(girl, renpy.random.choice(_pool))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 10)
        girl.set_flag("_cheating_trust_halfway_done")

    register_chitchat(
        "global",
        chitchat_ex_trust_halfway,
        condition=lambda g, loc, t: (
            getattr(g, "_ex_trust_max", 0) > 0
            and getattr(g, "_ex_trust", 0) >= getattr(g, "_ex_trust_max", 0) // 2
            and g.is_dating_player()
            and not g.get_flag("_cheating_trust_halfway_done")
        ),
        weight=15,
    )

    def chitchat_ex_trust_full(girl, loc, t_index):
        if getattr(girl, "_cheating_ex_reconciled", False):
            if girl.has_trait("loyal"):
                _pool = [
                    _("I trust you again. Fully. It took a long time, but you earned it. Every single day, you showed me you were different. I love you for that."),
                ]
            elif girl.has_trait("hardcore_sex"):
                _pool = [
                    _("Alright, listen. I'm done being suspicious. You proved yourself. We're good. For real this time. Don't you dare make me eat those words."),
                ]
            elif girl.has_trait("cute_sex"):
                _pool = [
                    _("I... I think I can trust you again. Completely. I was so scared for so long, but you never gave up on us. Thank you. I love you so much."),
                ]
            else:
                _pool = [
                    _("I think we're past it. The cheating, the suspicion, all of it. You put in the work, and I see that. I trust you again. Let's not waste it."),
                ]
            unlock_achievement("trust_rebuilt")
        else:
            _pool = [
                _("I think we're stronger now than before we broke up. Weird how that works, right?"),
                _("We made it. Through the breakup, the awkwardness, all of it. And here we are. Together."),
            ]
        set_scene_expression(girl, "happy")
        Say_Line(girl, renpy.random.choice(_pool))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 25)
        girl.set_flag("_cheating_trust_full_done")

    register_chitchat(
        "global",
        chitchat_ex_trust_full,
        condition=lambda g, loc, t: (
            getattr(g, "_ex_trust_max", 0) > 0
            and getattr(g, "_ex_trust", 0) >= getattr(g, "_ex_trust_max", 0)
            and g.is_dating_player()
            and not g.get_flag("_cheating_trust_full_done")
        ),
        weight=20,
    )

    # ── Girl-initiated confession (dating / harem request) ──

    def chitchat_girl_confesses(girl, loc, t_index):
        _gfs = get_player_girlfriends(ALL_GIRLS)
        _is_harem_ask = len(_gfs) >= 2

        # Approach dialogue by trait (date vs harem variants)
        if _is_harem_ask:
            if girl.has_trait("cute_sex"):
                _approach = [
                    _("I know you already have girlfriends... and I know this is a lot to ask... but I want to be part of that. Part of your life. Even if I have to share."),
                    _("I've seen how you are with the others. And... I want that too. I know it's complicated, but I don't care. I want in."),
                ]
            # telling him to add her is femdom, not hardcore (docs/plan_femdom.md D3)
            elif girl.has_trait("femdom"):
                _approach = [
                    _("Your little group. I want in. I've earned it. I've been patient, I've been good, and I've wanted this for a long time. Add me."),
                    _("You have girlfriends. Fine. Now you have one more. Me. Tell the others."),
                    _("I'm joining your group. I'm not asking permission, I'm telling you how this goes."),
                ]
            elif girl.has_trait("hardcore_sex"):
                _approach = [
                    _("Look, you've got multiple girlfriends. I'm not judging. I'm asking to be one of them. I can handle it."),
                    _("You've got a whole group of girlfriends? Good. I like a challenge. Let me in and I'll keep up with all of them."),
                ]
            elif girl.has_trait("loyal"):
                _approach = [
                    _("This is hard for me to say because I believe in being devoted to one person. But my person is you. And if sharing you is the price... I'll pay it."),
                    _("I never thought I'd ask something like this. But I'd rather share you than not have you at all. Please let me be part of your life."),
                ]
            elif girl.has_trait("cheater"):
                _approach = [
                    _("So... you have a few girlfriends already. I'm not blind. And honestly? I'd rather join the team than sit on the sidelines. If you'll have me."),
                    _("I know the situation is... unconventional. But I want to be with you, even if that means sharing. Can we make this work?"),
                ]
            else:
                _approach = [
                    _("I know you're already with other girls. I don't mind. I just want to be with you, even if it means sharing. Will you let me in?"),
                    _("I've been thinking about this for a while. I want to be your girlfriend, even if I'm not the only one. Is there room for me?"),
                ]
        else:
            if girl.has_trait("cute_sex"):
                _approach = [
                    _("Um... can I tell you something? I've been thinking about it for a while and... I really like you. Like, REALLY like you. Would you... want to be with me?"),
                    _("I practiced this in the mirror like fifty times... okay. Deep breath. I have feelings for you. Big ones. Do you... feel the same way?"),
                ]
            # claiming him ("you're mine") is femdom, not hardcore (docs/plan_femdom.md D3)
            elif girl.has_trait("femdom"):
                _approach = [
                    _("I don't do subtle. You're mine and I want everyone to know it. So... are we doing this or what?"),
                    _("I'm not asking twice. You're my boyfriend now. Say yes."),
                    _("Here's how this goes. You're with me now, officially. Any objections?"),
                ]
            elif girl.has_trait("hardcore_sex"):
                _approach = [
                    _("Alright, I'm just going to say it. I want you. Not just for fun. I want the whole thing. Girlfriend, boyfriend, the works. What do you say?"),
                    _("I'm not good at speeches, so here it is. I want you as my boyfriend. And yes, I still want it rough. Deal?"),
                ]
            elif girl.has_trait("loyal"):
                _approach = [
                    _("I need to tell you something serious. I've fallen for you. Completely. And I don't want to pretend I haven't anymore. Will you be with me?"),
                    _("This isn't a game to me. My feelings for you are real, and deep, and I can't keep them inside anymore. Will you be my boyfriend?"),
                ]
            elif girl.has_trait("cheater"):
                _approach = [
                    _("Don't make this weird, but... I kind of want to be your girlfriend. Loosely. Flexibly. You know what I mean."),
                    _("So here's the thing. I like you. More than I planned to. I'm not great at the whole 'commitment' thing, but... I want to try. With you."),
                ]
            else:
                _approach = [
                    _("I've been meaning to say this for a while. I like you. A lot. And I think we'd be good together. What do you think?"),
                    _("Can we talk about something? Us. I want there to be an us. Officially. What do you say?"),
                ]

        set_scene_expression(girl, "worried")
        Say_Line(girl, renpy.random.choice(_approach))

        _confess_result = renpy.display_menu([
            (_("Yes, I'd love that."), "accept"),
            (_("I like what we have now."), "gentle"),
            (_("That's not happening."), "cold"),
        ])

        if _confess_result == "accept":
            if _is_harem_ask:
                # Run GF voting
                _votes = []
                _blocked = False
                _blocking_gf = None
                for _gf in _gfs:
                    _vr, _vs, _vk = harem_vote_on_girl(_gf, girl)
                    _votes.append((_gf, _vr, _vs, _vk))
                    if _vr == "reject":
                        _blocked = True
                        _blocking_gf = _gf
                        break

                if _blocked and _blocking_gf:
                    set_scene_expression(_blocking_gf, "angry")
                    _block_lines = [
                        _("No way. I'm not sharing with HER."),
                        _("Absolutely not. I don't want her in our group."),
                        _("I refuse. She's not joining us."),
                    ]
                    Say_Line(_blocking_gf, renpy.random.choice(_block_lines))
                    set_scene_expression(_blocking_gf, "normal")
                    set_scene_expression(girl, "sad")
                    Say_Line(girl, _("I... I understand. Maybe another time."))
                    set_scene_expression(girl, "normal")
                    girl._confess_cooldown_day = store.Day
                    girl._confess_reject_count = getattr(girl, "_confess_reject_count", 0) + 1
                    return

                # All approved — add to harem
                for _gf in _gfs:
                    add_to_harem(_gf, girl.gid)
                    add_to_harem(girl, _gf.gid)

                girl.Player_status = "dating"
                girl._open_relationship_consent = True
                Player.discover("first_girlfriend")
                girl.discover("discovered_dating_player")
                girl.discover("discovered_relationship")

                _ad_hg = _get_harem_group()
                if _ad_hg is None:
                    _create_harem_group(_gfs[0])
                    _ad_hg = _get_harem_group()
                    if _ad_hg and girl.gid not in _ad_hg["members"]:
                        _ad_hg["members"].append(girl.gid)
                elif girl.gid not in _ad_hg["members"]:
                    _ad_hg["members"].append(girl.gid)
                if _ad_hg:
                    _store_group_tiers(_ad_hg["id"], _ad_hg["members"])

                _update_relationship_mode()
                print("[CONFESS] %s joined harem via confession" % girl.gid)
            else:
                # Simple dating
                girl.Player_status = "dating"
                Player.discover("first_girlfriend")
                girl.discover("discovered_dating_player")
                girl.discover("discovered_relationship")
                _update_relationship_mode()
                print("[CONFESS] %s started dating via confession" % girl.gid)

            set_scene_expression(girl, "happy")
            Say_Line(girl, rod_pick_line(girl, "confess_love_accept"))
            Change_Status(girl, "Love", 30)
            Change_Status(girl, "Obed", 10)
            unlock_achievement("she_came_to_me")

        elif _confess_result == "gentle":
            set_scene_expression(girl, "sad")
            Say_Line(girl, rod_pick_line(girl, "confess_love_reject"))
            set_scene_expression(girl, "normal")
            Change_Status(girl, "Love", 5)
            girl._confess_cooldown_day = store.Day
            girl._confess_reject_count = getattr(girl, "_confess_reject_count", 0) + 1
            print("[CONFESS] %s gentle rejected (count=%d)" % (girl.gid, girl._confess_reject_count))

        else:  # cold
            _cold_lines = [
                _("Oh... okay. I get it. I won't bring it up again. Ever."),
                _("...Wow. Alright then. Message received. Loud and clear."),
                _("That was... harsh. But fine. I know where I stand now."),
            ]
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice(_cold_lines))
            set_scene_expression(girl, "normal")
            Change_Status(girl, "Love", -30)
            Change_Status(girl, "Obed", -20)
            girl._confess_permanent_stop = True
            print("[CONFESS] %s cold rejected, permanent stop" % girl.gid)

        set_scene_expression(girl, "normal")

    register_chitchat(
        "global",
        chitchat_girl_confesses,
        condition=lambda g, loc, t: (
            not g.is_dating_player()
            # taken: same rule as the player's own "Will you be my girlfriend?" (_ask_date refuses while she has a
            # partner); accepting here made her date him AND her partner at once
            and not (hasattr(g, "has_npc_partner") and g.has_npc_partner())
            and not (hasattr(g, "has_girl_partner") and g.has_girl_partner())
            and not g.has_trait("lesbian")
            # married: she does not date him (MARRIED_DATE_REFUSE, docs/plan_shion.md D6)
            and not g.has_trait("married")
            and not getattr(g, "_confess_permanent_stop", False)
            and getattr(g, "Love", 0) >= CONFESSION_CONFIG["love_min"]
            and getattr(g, "Obed", 0) >= (CONFESSION_CONFIG["obed_harem_min"] if len(get_player_girlfriends(ALL_GIRLS)) >= 2 else CONFESSION_CONFIG["obed_single_min"])
            and not g.has_temp_status("angry")
            and not g.has_temp_status("sad")
            and (store.Day - getattr(g, "_confess_cooldown_day", 0)) >= CONFESSION_CONFIG["cooldown_days"]
            and getattr(g, "_confess_reject_count", 0) < CONFESSION_CONFIG["max_gentle_rejects"]
            and len(get_player_girlfriends(ALL_GIRLS)) != 1
            and (len(get_player_girlfriends(ALL_GIRLS)) < 2 or not g.has_trait("monogamous"))
            and (getattr(g, "Sex_acts", None) or {}).get("kiss", 0) >= CONFESSION_CONFIG["min_kiss"]
            and (getattr(g, "Sex_acts", None) or {}).get("sex", 0) >= CONFESSION_CONFIG["min_sex"]
        ),
        weight=25,
    )

    # ============================================================
    # GET TO KNOW HER — Player asks about the girl (Tipo A)
    # ============================================================

    # Her own answer to a question below, where no trait of hers answers first (author canon, docs/Personality.md).
    # A girl or a question missing here keeps the generic answers. Never a {hint}: the trait answers carry those.
    # One line each: every question is asked once per girl (the _cc_asked_* flag).
    _CC_ASK_STYLE = {
        "gwen": {
            "family": [_("We're fine. My mom still calls my drawings 'interesting'. She means it as a compliment. I think.")],
            "music": [_("Dark stuff. Post-punk, goth rock, anything with a little heartbreak in it.")],
            "bored": [_("Draw. Always. I carry a sketchbook everywhere for exactly that reason.")],
            "fav_place": [_("The old bench behind the library. Quiet, shady, and nobody reads over my shoulder while I draw.")],
        },
        "rogue": {
            "family": [_("It's... complicated. My aunt raised me, mostly. The rest of my blood family is a longer story, sugar.")],
            "music": [_("Southern rock and a little old country, sugar. My aunt had the radio on from sunup to sundown.")],
            "bored": [_("Get outside. A long walk, some fresh air... I'd go ridin' if there was a horse anywhere near this campus.")],
            "fav_place": [_("Anywhere outdoors. Under a big tree with some shade and nobody in a hurry.")],
            "cooking": [_("I cook, sugar. My aunt made sure. Biscuits, gravy, fried chicken... you behave and I might feed you.")],
        },
        "ntw": {
            "family": [_("Define 'family'. I grew up around people who trained me. A couple of them count.")],
            "music": [_("Industrial metal. Loud enough to drown everyone out.")],
            "bored": [_("Take something electronic apart and put it back together better.")],
            "fav_place": [_("The gym at 6 AM. Nobody talks to you at 6 AM.")],
            "cooking": [_("Microwave. Hot sauce. Done.")],
        },
        "tenny": {
            "family": [_("Really close. My parents are the sensible ones, my grandpa is the adventure. I miss all of them.")],
            "music": [_("Film scores. Perfect for studying. Space documentaries count too, if you ask me.")],
            "bored": [_("Research something I have absolutely no reason to know. Last week it was ancient calendars.")],
            "fav_place": [_("The roof after dark. Best view of the stars on campus. Don't tell anyone.")],
            "cooking": [_("I follow recipes like lab protocols. Measured to the gram. My grandpa just throws things in a pan and hopes.")],
        },
        # Shion: his stepmother (docs/plan_shion.md), before she turns. Not a student: "on campus" gets her office
        "shion": {
            "family": [_("I married into yours, remember? Close enough to see every grade you get. That's as close as I need to be.")],
            "music": [_("Opera. Season tickets, a private box. Your father snores through the second act, so I pinch him until he stops.")],
            "bored": [_("I don't get bored. I go through my staff and decide who's replaceable. Someone always is.")],
            "fav_place": [_("On campus? Nowhere. My favorite spot is the top floor of my building, where everyone else is below me.")],
            "cooking": [_("I have a chef on speed dial and a husband who thinks the microwave counts as cooking. Guess which one feeds me.")],
        },
    }

    def _cc_ask_style(girl, key, generic):
        """One answer to question `key`: hers when her style has one, else one of the generic ones."""
        _pool = _CC_ASK_STYLE.get(getattr(girl, "gid", ""), {}).get(key) or generic
        return renpy.random.choice(_pool)

    # --- Low gate (Love >= 50) ---

    def cc_ask_music(girl, loc, t_index):
        Say_Player(_("What kind of music are you into?"))
        if girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("Anything loud. I need to feel the bass in my chest."), _("Rock, metal... anything with energy. The heavier the better.")]))
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("Indie stuff, lo-fi... things that make you feel warm."), _("Soft pop, acoustic... I like songs that tell a story.")]))
        else:
            Say_Line(girl, _cc_ask_style(girl, "music", [_("A bit of everything, honestly. Depends on my mood."), _("Whatever's on the radio. I'm not picky.")]))
        Change_Status(girl, "Love", 2)
        girl._cc_asked_music = True

    def cc_ask_cooking(girl, loc, t_index):
        Say_Player(_("Do you cook or are you a takeout person?"))
        if girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("I try to cook! It doesn't always work out, but I like it."), _("I bake a lot. Cookies, cakes... want to try some next time?")]))
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("Takeout. Life's too short to stand over a stove."), _("I can cook, I just don't want to. That's what delivery is for.")]))
        else:
            Say_Line(girl, _cc_ask_style(girl, "cooking", [_("I cook sometimes. Nothing fancy, but I survive."), _("Depends on the day. If I'm tired, takeout wins.")]))
        Change_Status(girl, "Love", 2)
        girl._cc_asked_cooking = True

    def cc_ask_morning_night(girl, loc, t_index):
        Say_Player(_("Morning person or night owl?"))
        if girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("Night. Nothing good happens before noon."), _("I come alive when the sun goes down. Make of that what you will.")]))
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("Morning! I love the quiet before everyone wakes up."), _("Early bird... mostly because I can't sleep in even if I try.")]))
        else:
            Say_Line(girl, renpy.random.choice([_("Depends on the semester. Exams make me nocturnal."), _("Somewhere in between. I'm functional by 10 AM.")]))
        Change_Status(girl, "Love", 1)
        girl._cc_asked_morning = True

    def cc_ask_bored(girl, loc, t_index):
        Say_Player(_("What do you do when you're bored?"))
        if girl.has_trait("public_fetish") or girl.has_trait("exhibitionist"):
            Say_Line(girl, renpy.random.choice([_("Go out. {hint}I need people around me{/hint}. Staying in drives me crazy."), _("People-watch. {hint}There's something exciting about being out in the open{/hint}.")]))
            if girl.has_trait("public_fetish"):
                girl.discover("discovered_trait_public_fetish")
            if girl.has_trait("exhibitionist"):
                girl.discover("discovered_trait_exhibitionist")
        elif girl.has_trait("camera_lover"):
            Say_Line(girl, renpy.random.choice([_("{hint}Take photos{/hint}. My phone is full of random shots."), _("{hint}Scroll through my camera roll{/hint} and relive memories. I'm sentimental like that.")]))
            girl.discover("discovered_trait_camera_lover")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("Read, draw, take naps... I'm pretty low-key."), _("Daydream, mostly. My mind wanders to weird places.")]))
        else:
            Say_Line(girl, _cc_ask_style(girl, "bored", [_("Scroll my phone until I hate myself for wasting time."), _("Find someone to hang out with. Boredom is a two-person problem.")]))
        Change_Status(girl, "Love", 2)
        girl._cc_asked_bored = True

    def cc_ask_fav_place(girl, loc, t_index):
        Say_Player(_("What's your favorite spot on campus?"))
        if girl.has_trait("public_shy"):
            Say_Line(girl, renpy.random.choice([_("The library, back corner. {hint}Nobody bothers me there{/hint}."), _("My room. {hint}I like my privacy{/hint}.")]))
            girl.discover("discovered_trait_public_shy")
        elif girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([_("The pool area. {hint}I love being seen{/hint}... in a swimsuit or whatever."), _("Anywhere with people. {hint}The energy of a crowd does something to me{/hint}.")]))
            girl.discover("discovered_trait_public_fetish")
        else:
            Say_Line(girl, _cc_ask_style(girl, "fav_place", [_("The rooftop, if you can get up there. Best view."), _("The cafeteria. Food and gossip, what more do you need?")]))
        Change_Status(girl, "Love", 2)
        girl._cc_asked_fav_place = True

    # --- Medium gate (Love >= 150) ---

    def cc_ask_perfect_date(girl, loc, t_index):
        Say_Player(_("What's your idea of a perfect date?"))
        if girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("Skip dinner. {hint}Take me somewhere exciting{/hint}. I don't need flowers."), _("Something spontaneous. {hint}I hate planned, romantic crap{/hint}. Surprise me.")]))
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("Dinner, a walk, maybe stargazing... {hint}I'm a hopeless romantic{/hint}."), _("Something simple. {hint}Cook for me, hold my hand{/hint}... that's all I need.")]))
            girl.discover("discovered_trait_cute_sex")
        else:
            Say_Line(girl, renpy.random.choice([_("Good food, good company. I'm not complicated."), _("Anything where we can actually talk. No movies on a first date.")]))
        Change_Status(girl, "Love", 3)
        girl._cc_asked_date = True

    def cc_ask_family(girl, loc, t_index):
        Say_Player(_("Are you close with your family?"))
        Say_Line(girl, _cc_ask_style(girl, "family", [_("It's... complicated. We talk, but there's distance."), _("Yeah, they're great. I miss them."), _("Not really. I'm better on my own.")]))
        Change_Status(girl, "Love", 3)
        girl._cc_asked_family = True

    def cc_ask_pet_peeve(girl, loc, t_index):
        Say_Player(_("What's your biggest pet peeve?"))
        if girl.has_trait("camera_hater"):
            Say_Line(girl, renpy.random.choice([_("People who {hint}film everything{/hint}. Put the phone down and live your life."), _("{hint}Being photographed without permission{/hint}. That drives me insane.")]))
            girl.discover("discovered_trait_camera_hater")
        elif girl.has_trait("hate_cum"):
            Say_Line(girl, renpy.random.choice([_("People who don't clean up after themselves. {hint}I hate messes{/hint}."), _("{hint}Gross stuff{/hint}. I can't handle anything... messy. Even talking about it.")]))
            girl.discover("discovered_trait_hate_cum")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("People who can't make decisions. Just commit to something."), _("Being bored. If something isn't exciting, why bother?")]))
        else:
            Say_Line(girl, renpy.random.choice([_("Being ignored mid-conversation. It's so rude."), _("Loud chewing. I know it's dumb but it kills me.")]))
        Change_Status(girl, "Love", 2)
        girl._cc_asked_peeve = True

    def cc_ask_trust(girl, loc, t_index):
        Say_Player(_("Do you trust people easily?"))
        if girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([_("{hint}When I trust someone, I trust them completely{/hint}. That's just how I am."), _("Yes. Maybe too much. {hint}I believe in loyalty{/hint}.")]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("cheater"):
            Say_Line(girl, renpy.random.choice([_("Trust is earned. And lost easily."), _("I've learned that people aren't always what they seem. {hint}Including me{/hint}.")]))
            girl.discover("discovered_trait_cheater")
        else:
            Say_Line(girl, renpy.random.choice([_("Depends on the person. You have to show me you're worth trusting."), _("It takes time. But once you're in, you're in.")]))
        Change_Status(girl, "Love", 3)
        girl._cc_asked_trust = True

    def cc_ask_regret(girl, loc, t_index):
        Say_Player(_("Have you ever done something you really regret?"))
        set_scene_expression(girl, "shy")
        if girl.has_trait("cheater") and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            Say_Line(girl, renpy.random.choice([_("...Yes. Something I can't take back. And I'd probably do it again."), _("More than once. I'm not as good a person as people think.")]))
            girl.discover("discovered_trait_cheater")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("A few small things... I overthink everything, so they feel bigger than they are."), _("Sometimes I wish I'd been braver. I play it too safe.")]))
        else:
            Say_Line(girl, renpy.random.choice([_("Everyone has regrets. I try not to dwell on them."), _("Yeah. But I'd rather not talk about it.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)
        girl._cc_asked_regret = True

    # --- High gate (Love >= 300, Inbt >= 200) ---

    def cc_ask_guilty_pleasure(girl, loc, t_index):
        Say_Player(_("Come on, tell me your guilty pleasure."))
        set_scene_expression(girl, "shy")
        if girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([_("Doing things {hint}where someone might see{/hint}. The risk is... exciting."), _("Walking around in {hint}something revealing{/hint} and pretending I don't notice people staring.")]))
            girl.discover("discovered_trait_public_fetish")
        elif girl.has_trait("camera_lover"):
            Say_Line(girl, renpy.random.choice([_("{hint}Taking photos of myself{/hint} when nobody's watching. More than I'd ever admit."), _("Reviewing {hint}videos{/hint} I've taken. Some of them are... private.")]))
            girl.discover("discovered_trait_camera_lover")
        elif girl.has_trait("cum_slut"):
            Say_Line(girl, renpy.random.choice([_("I have... specific tastes. {hint}Physical ones{/hint}. I'll tell you when I trust you more."), _("Something I can't say out loud yet. Ask me again when we know each other better.")]))
            girl.discover("discovered_trait_cum_slut")
        else:
            Say_Line(girl, renpy.random.choice([_("Trash TV. Hours of it. Don't judge me."), _("Eating an entire pizza alone at 2 AM. Peak performance.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 2)
        girl._cc_asked_guilty = True

    def cc_ask_adventurous(girl, loc, t_index):
        Say_Player(_("Would you say you're adventurous or do you play it safe?"))
        if girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("{hint}Adventurous. Always{/hint}. Playing it safe is boring."), _("I push boundaries. {hint}That's where the fun is{/hint}.")]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("{hint}Safe, usually{/hint}. But sometimes I want to be brave..."), _("I play it safe. But... {hint}with the right person, I'd try things{/hint}.")]))
            girl.discover("discovered_trait_cute_sex")
        else:
            Say_Line(girl, renpy.random.choice([_("Depends on what we're talking about. Life? Adventurous. Heights? No."), _("A healthy mix. I know my limits but I'm not afraid to test them.")]))
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 2)
        girl._cc_asked_adventurous = True

    def cc_ask_boldest(girl, loc, t_index):
        Say_Player(_("What's the boldest thing you've ever done?"))
        set_scene_expression(girl, "shy")
        if girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([_("Something... {hint}in a place where anyone could have seen{/hint}. My heart was pounding."), _("I did something really risky {hint}in public once{/hint}. I can't stop thinking about it.")]))
            girl.discover("discovered_trait_public_fetish")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("I said yes to something most people would say no to. No regrets."), _("Something intense. {hint}I like pushing past my comfort zone{/hint}.")]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("I... confessed to someone once. My voice was shaking the whole time."), _("Wore something way outside my comfort zone. I was red the entire day.")]))
        else:
            Say_Line(girl, renpy.random.choice([_("Skinny dipping. Once. Never again... maybe."), _("Talked back to a professor in front of the whole class. Felt amazing.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 3)
        girl._cc_asked_boldest = True

    def cc_ask_jealous(girl, loc, t_index):
        Say_Player(_("Do you get jealous easily?"))
        if girl.has_trait("loyal"):
            Say_Line(girl, renpy.random.choice([_("{hint}Yes{/hint}. If I'm with someone, {hint}I'm all in{/hint}. And I expect the same."), _("More than I'd like to admit. {hint}I care too much{/hint}.")]))
            girl.discover("discovered_trait_loyal")
        elif girl.has_trait("cheater"):
            Say_Line(girl, renpy.random.choice([_("Not really. {hint}I don't have the right to be{/hint}, honestly."), _("Jealousy is pointless. {hint}People do what they want{/hint}.")]))
            girl.discover("discovered_trait_cheater")
        else:
            Say_Line(girl, renpy.random.choice([_("A little. I try to hide it, but yeah."), _("Depends on the person. If I really like them... yes.")]))
        Change_Status(girl, "Love", 2)
        girl._cc_asked_jealous = True

    def cc_ask_sharing(girl, loc, t_index):
        Say_Player(_("How would you feel about sharing a partner with someone else?"))
        set_scene_expression(girl, "serious")
        if girl.has_trait("polyamorous"):
            Say_Line(girl, renpy.random.choice([_("{hint}I'm actually okay with it{/hint}. Love doesn't have to be exclusive, you know?"), _("{hint}Sharing doesn't scare me{/hint}. As long as everyone's honest, I think it can work.")]))
            girl.discover("discovered_trait_polyamorous")
        elif girl.has_trait("monogamous"):
            Say_Line(girl, renpy.random.choice([_("{hint}Absolutely not{/hint}. If I'm with someone, {hint}they're mine and I'm theirs{/hint}. Period."), _("{hint}That's a dealbreaker for me{/hint}. I believe in {hint}one person, one heart{/hint}. No exceptions.")]))
            girl.discover("discovered_trait_monogamous")
        else:
            Say_Line(girl, renpy.random.choice([_("I don't know... I've never really thought about it. Maybe? Depends on the situation."), _("That's a weird question. I guess it would depend on how I felt about the person.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        girl._cc_asked_sharing = True

    def cc_ask_hard_limits(girl, loc, t_index):
        Say_Player(_("Is there anything you'd never do, no matter what?"))
        set_scene_expression(girl, "serious")
        if girl.has_trait("anal_hater"):
            Say_Line(girl, renpy.random.choice([_("{hint}Certain things are off limits{/hint}. Permanently. Don't even ask."), _("There's one thing I {hint}absolutely refuse{/hint}. And I mean it.")]))
            girl.discover("discovered_trait_anal_hater")
        elif girl.has_trait("hate_cum"):
            Say_Line(girl, renpy.random.choice([_("Anything {hint}messy{/hint}. I have a thing about... {hint}cleanliness{/hint}. During everything."), _("There are certain... {hint}physical things{/hint} I just can't handle. Ever.")]))
            girl.discover("discovered_trait_hate_cum")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("Honestly? Not much. {hint}I'm open to almost anything{/hint}."), _("{hint}My limits are pretty far out there{/hint}. You'd have to try hard to find them.")]))
            girl.discover("discovered_trait_hardcore_sex")
        else:
            Say_Line(girl, renpy.random.choice([_("A few things. But I'd rather not list them out."), _("Everyone has lines they won't cross. I have mine.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 3)
        girl._cc_asked_limits = True

    # --- Intimate gate (Love >= 500, Inbt >= 400) ---

    def cc_ask_turn_on(girl, loc, t_index):
        Say_Player(_("Okay, real talk. What really turns you on?"))
        set_scene_expression(girl, "sexy")
        if girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("{hint}Being pushed around a little{/hint}. I like it rough. Don't be gentle."), _("{hint}Intensity{/hint}. I want to feel it the next day.")]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("{hint}Slow, gentle, intimate{/hint}... eye contact. Being held."), _("{hint}Feeling safe{/hint}. When I trust someone completely... that's when I let go.")]))
            girl.discover("discovered_trait_cute_sex")
        elif girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([_("{hint}The risk of being caught{/hint}. My heart races just thinking about it."), _("Doing things {hint}where we shouldn't{/hint}. The danger is the turn-on.")]))
            girl.discover("discovered_trait_public_fetish")
        else:
            Say_Line(girl, renpy.random.choice([_("Confidence. Someone who knows what they want and takes it."), _("Chemistry. When the tension is so thick you can barely breathe.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)
        Change_Status(girl, "Inbt", 5)
        girl._cc_asked_turnon = True

    def cc_ask_control(girl, loc, t_index):
        Say_Player(_("Do you like being in control or giving it up?"))
        set_scene_expression(girl, "sexy")
        # being in control is femdom (docs/plan_femdom.md 7): the question reveals it. Still discovering it (D7),
        # she is only finding out she likes being in charge; a veteran knows
        if girl.has_trait("femdom"):
            if trait_is_veteran(girl, "femdom"):
                set_scene_expression(girl, "smug")
                Say_Line(girl, renpy.random.choice([
                    _("In control. Always. {hint}I give the orders{/hint}, you follow them."),
                    _("Giving it up? Cute question. {hint}I'm the one in charge{/hint}. That's not up for debate."),
                    _("In control. {hint}I like deciding everything{/hint}. When, how, how fast... and when you're allowed to stop."),
                ]))
            else:
                set_scene_expression(girl, "embarrassed")
                Say_Line(girl, renpy.random.choice([
                    _("Lately? {hint}I want to be the one in charge{/hint}. That's new for me... and I kind of love it."),
                    _("I'm still figuring it out. But {hint}telling someone what to do{/hint}... I like it more than I expected."),
                    _("In control, I think? {hint}I'm only now finding out I like giving orders{/hint}. Is that weird?"),
                ]))
            print("[FEMDOM] %s answers cc_ask_control as a femdom (veteran=%s)" % (girl.gid, trait_is_veteran(girl, "femdom")))
            girl.discover("discovered_trait_femdom")
        # giving up control is submissive, not hardcore (docs/plan_femdom.md D3): hardcore only cares that it is rough
        elif girl.has_trait("submissive"):
            Say_Line(girl, renpy.random.choice([_("{hint}I like giving it up{/hint}. Completely. Take over."), _("Both. But if I had to choose... {hint}make me submit{/hint}.")]))
            girl.discover("discovered_trait_submissive")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("I don't care who's in charge. {hint}I care that it's rough{/hint}."), _("Leading, following... whatever. {hint}Just don't be gentle with me{/hint}.")]))
            girl.discover("discovered_trait_hardcore_sex")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("I like when someone else leads... {hint}gently{/hint}. I trust them to take care of me."), _("{hint}I don't want to be in charge{/hint}. Just... be sweet about it.")]))
            girl.discover("discovered_trait_cute_sex")
        else:
            Say_Line(girl, renpy.random.choice([_("Depends on my mood. Sometimes I want to lead, sometimes I want to follow."), _("I like switching. Keeps things interesting.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)
        Change_Status(girl, "Inbt", 5)
        girl._cc_asked_control = True

    def cc_ask_fantasy(girl, loc, t_index):
        Say_Player(_("What's your biggest fantasy?"))
        set_scene_expression(girl, "shy")
        if girl.has_trait("public_fetish"):
            Say_Line(girl, renpy.random.choice([_("Being... {hint}taken somewhere public{/hint}. Where anyone could walk in."), _("Something {hint}outside{/hint}. Under the stars. With the risk of being seen.")]))
            girl.discover("discovered_trait_public_fetish")
        elif girl.has_trait("anal_lover"):
            Say_Line(girl, renpy.random.choice([_("Something... {hint}from behind{/hint}. All the way. I've thought about it more than I should."), _("Being completely {hint}used{/hint}. In ways most girls won't admit they want.")]))
            girl.discover("discovered_trait_anal_lover")
        elif girl.has_trait("camera_lover"):
            Say_Line(girl, renpy.random.choice([_("Being {hint}filmed{/hint}. Having proof that it happened. Watching it back later."), _("{hint}Recording{/hint} something really intimate. For my eyes only. Maybe.")]))
            girl.discover("discovered_trait_camera_lover")
        elif girl.has_trait("cute_sex"):
            Say_Line(girl, renpy.random.choice([_("Being... completely devoted to someone. Making love all night. Just us."), _("Slow, passionate, endless... I want to feel loved, not just wanted.")]))
        else:
            Say_Line(girl, renpy.random.choice([_("Something I'll tell you if you earn it."), _("I have one. But you'll have to get closer to me before I share.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)
        Change_Status(girl, "Inbt", 5)
        girl._cc_asked_fantasy = True

    def cc_ask_want_to_try(girl, loc, t_index):
        Say_Player(_("Is there anything you've always wanted to try?"))
        set_scene_expression(girl, "shy")
        if girl.has_trait("anal_lover"):
            Say_Line(girl, renpy.random.choice([_("There's... {hint}something most people don't talk about{/hint}. But I think about it a lot."), _("Something {hint}taboo{/hint}. I've been curious for a long time. Don't judge me.")]))
            girl.discover("discovered_trait_anal_lover")
        elif girl.has_trait("cum_slut"):
            Say_Line(girl, renpy.random.choice([_("I want to try... {hint}everything{/hint}. And I mean everything. No holding back."), _("Being completely {hint}covered{/hint}. Marked. {hint}Claimed{/hint}. I know it sounds crazy.")]))
            girl.discover("discovered_trait_cum_slut")
        elif girl.has_trait("hardcore_sex"):
            Say_Line(girl, renpy.random.choice([_("Something that would make most people uncomfortable. {hint}I want to be pushed{/hint}."), _("I've always wanted to go {hint}way past my comfort zone{/hint}. With someone I trust.")]))
            girl.discover("discovered_trait_hardcore_sex")
        else:
            Say_Line(girl, renpy.random.choice([_("Maybe something outside my comfort zone. With the right person."), _("I don't know yet. But I feel like I'll know when the moment comes.")]))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)
        Change_Status(girl, "Inbt", 5)
        girl._cc_asked_try = True

    # ============================================================
    # GIRL ASKS PLAYER — Quiz mechanic (Tipo B)
    # ============================================================

    def cc_girl_asks_type(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("So... what's your type?"))
        _is_cute = girl.has_trait("cute_sex")
        _is_hc = girl.has_trait("hardcore_sex")
        _choice = renpy.display_menu([
            (_("Sweet and gentle"), "sweet"),
            (_("Wild and intense"), "wild"),
            (_("I don't have a type"), "none"),
        ])
        if _choice == "sweet" and _is_cute:
            Say_Line(girl, renpy.random.choice([_("Really? That's... that's good to know."), _("You like sweet girls? I think I can work with that.")]))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 3)
        elif _choice == "wild" and _is_hc:
            Say_Line(girl, renpy.random.choice([_("Good answer."), _("Now you're speaking my language.")]))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 3)
        elif _choice == "none":
            Say_Line(girl, renpy.random.choice([_("Diplomatic. I see you."), _("That's either very open-minded or very lazy.")]))
            Change_Status(girl, "Love", 1)
        else:
            Say_Line(girl, renpy.random.choice([_("Hm. Interesting."), _("Really? That's... not what I expected.")]))
            Change_Status(girl, "Love", -2)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_type = True

    def cc_girl_asks_pretty(girl, loc, t_index):
        set_scene_expression(girl, "shy")
        Say_Line(girl, renpy.random.choice([_("Be honest with me... am I pretty?"), _("Do you think I'm attractive? Like, actually?")]))
        _choice = renpy.display_menu([
            (_("You're beautiful"), "beautiful"),
            (_("You're okay"), "okay"),
            (_("Fishing for compliments?"), "fishing"),
        ])
        if _choice == "beautiful":
            set_scene_expression(girl, "happy")
            Say_Line(girl, renpy.random.choice([_("You mean that? ...Thank you."), _("That actually means a lot coming from you.")]))
            Change_Status(girl, "Love", 5)
        elif _choice == "fishing":
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([_("Maybe I am. You still didn't answer though."), _("Deflecting! But I'll take that as a yes.")]))
            Change_Status(girl, "Love", 2)
        else:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([_("Just... okay? Wow."), _("That's not exactly what a girl wants to hear.")]))
            Change_Status(girl, "Love", -3)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_pretty = True

    def cc_girl_asks_first_notice(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("What did you first notice about me?"))
        _is_cute = girl.has_trait("cute_sex")
        _is_hc = girl.has_trait("hardcore_sex")
        _choice = renpy.display_menu([
            (_("Your smile"), "smile"),
            (_("Your body"), "body"),
            (_("Your personality"), "personality"),
        ])
        if _choice == "smile" and _is_cute:
            set_scene_expression(girl, "happy")
            Say_Line(girl, renpy.random.choice([_("That's so sweet..."), _("Nobody ever says that. I love that you noticed.")]))
            Change_Status(girl, "Love", 5)
        elif _choice == "body" and _is_hc:
            set_scene_expression(girl, "sexy")
            Say_Line(girl, renpy.random.choice([_("At least you're honest. I respect that."), _("Good. I work hard on it.")]))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Inbt", 3)
        elif _choice == "personality":
            Say_Line(girl, renpy.random.choice([_("That's a safe answer... but I'll take it."), _("Smooth. Very smooth.")]))
            Change_Status(girl, "Love", 3)
        elif _choice == "body" and _is_cute:
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([_("M-my body? That's... um..."), _("I wasn't expecting that... you're making me blush.")]))
            Change_Status(girl, "Love", -1)
            Change_Status(girl, "Inbt", 2)
        elif _choice == "smile" and _is_hc:
            Say_Line(girl, renpy.random.choice([_("My smile? That's... unexpectedly sweet."), _("Huh. Didn't take you for the romantic type.")]))
            Change_Status(girl, "Love", 3)
        else:
            Say_Line(girl, renpy.random.choice([_("Good answer."), _("I can live with that.")]))
            Change_Status(girl, "Love", 2)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_notice = True

    def cc_girl_asks_dating(girl, loc, t_index):
        set_scene_expression(girl, "smile")
        Say_Line(girl, _("Would you be jealous if I talked to other guys?"))
        _is_loyal = girl.has_trait("loyal")
        _choice = renpy.display_menu([
            (_("Yes, honestly"), "yes"),
            (_("No, you're free to do whatever"), "no"),
            (_("A little, maybe"), "little"),
        ])
        if _choice == "yes":
            if _is_loyal:
                set_scene_expression(girl, "happy")
                Say_Line(girl, renpy.random.choice([_("That's actually really reassuring."), _("Good. I'd be jealous too.")]))
                Change_Status(girl, "Love", 5)
            else:
                Say_Line(girl, renpy.random.choice([_("Possessive. Noted."), _("That's... a lot. But kind of flattering.")]))
                Change_Status(girl, "Love", 2)
        elif _choice == "no":
            if _is_loyal:
                set_scene_expression(girl, "sad")
                Say_Line(girl, renpy.random.choice([_("You wouldn't care at all? ...Oh."), _("That's... not what I hoped you'd say.")]))
                Change_Status(girl, "Love", -3)
            else:
                Say_Line(girl, renpy.random.choice([_("Mature. I like that."), _("Good. I don't do possessive.")]))
                Change_Status(girl, "Love", 2)
                Change_Status(girl, "Inbt", 2)
        else:
            Say_Line(girl, renpy.random.choice([_("Honest. I appreciate that."), _("That's a fair answer.")]))
            Change_Status(girl, "Love", 3)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_jealous = True

    def cc_girl_asks_boring(girl, loc, t_index):
        set_scene_expression(girl, "shy")
        Say_Line(girl, _("Be honest... do you think I'm boring?"))
        _choice = renpy.display_menu([
            (_("Never"), "never"),
            (_("You have your moments"), "moments"),
            (_("Sometimes, yeah"), "sometimes"),
        ])
        if _choice == "never":
            set_scene_expression(girl, "happy")
            Say_Line(girl, renpy.random.choice([_("You're sweet. I needed to hear that."), _("Really? ...That makes me happy.")]))
            Change_Status(girl, "Love", 5)
        elif _choice == "moments":
            Say_Line(girl, renpy.random.choice([_("Okay, I'll take that. At least I'm not ALWAYS boring."), _("Fair enough. I'll try to keep you entertained.")]))
            Change_Status(girl, "Love", 1)
        else:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([_("...Ouch. That actually hurt."), _("Wow. Thanks for the honesty, I guess.")]))
            Change_Status(girl, "Love", -5)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_boring = True

    def cc_girl_asks_spend_time(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("Do you actually like spending time with me? Or are you just bored?"))
        _choice = renpy.display_menu([
            (_("More than anything"), "more"),
            (_("It's alright"), "alright"),
            (_("I wouldn't be here if I didn't"), "proof"),
        ])
        if _choice == "more":
            set_scene_expression(girl, "happy")
            Say_Line(girl, renpy.random.choice([_("...That's the best thing anyone's said to me in a while."), _("You really mean that? I... I like spending time with you too.")]))
            Change_Status(girl, "Love", 7)
        elif _choice == "proof":
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([_("Point taken. Actions speak louder."), _("That's true. You keep showing up. That says enough.")]))
            Change_Status(girl, "Love", 4)
        else:
            set_scene_expression(girl, "sad")
            Say_Line(girl, renpy.random.choice([_("Just... alright? Okay then."), _("I'll pretend that didn't sting.")]))
            Change_Status(girl, "Love", -3)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_time = True

    def cc_girl_asks_crazy(girl, loc, t_index):
        set_scene_expression(girl, "sexy")
        Say_Line(girl, _("What's the craziest thing you'd do with me?"))
        _is_pub = girl.has_trait("public_fetish")
        _is_cute = girl.has_trait("cute_sex")
        _choice = renpy.display_menu([
            (_("Anything you want"), "anything"),
            (_("Something in public"), "public"),
            (_("Something private and intense"), "private"),
        ])
        if _choice == "public" and _is_pub:
            Say_Line(girl, renpy.random.choice([_("You read my mind."), _("Now THAT is the right answer.")]))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 5)
        elif _choice == "private" and _is_cute:
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([_("Private and intense... that sounds perfect."), _("Just the two of us... yes. That's what I want.")]))
            Change_Status(girl, "Love", 5)
            Change_Status(girl, "Inbt", 3)
        elif _choice == "anything":
            Say_Line(girl, renpy.random.choice([_("Careful what you promise. I might hold you to that."), _("Anything? That's a dangerous word. I like it.")]))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Inbt", 3)
        elif _choice == "public" and _is_cute:
            set_scene_expression(girl, "shy")
            Say_Line(girl, renpy.random.choice([_("In public?! That's... I don't think I could..."), _("I'd die of embarrassment... but you'd want that, wouldn't you.")]))
            Change_Status(girl, "Love", -1)
        else:
            Say_Line(girl, renpy.random.choice([_("Interesting choice. I'll keep that in mind."), _("Noted. We might have to negotiate on that.")]))
            Change_Status(girl, "Love", 2)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_crazy = True

    def cc_girl_asks_good_in_bed(girl, loc, t_index):
        set_scene_expression(girl, "sexy")
        Say_Line(girl, renpy.random.choice([_("So... am I good in bed?"), _("Rate my performance. Honestly.")]))
        _choice = renpy.display_menu([
            (_("Amazing"), "amazing"),
            (_("We could try new things"), "new"),
            (_("You need practice"), "practice"),
        ])
        if _choice == "amazing":
            set_scene_expression(girl, "happy")
            Say_Line(girl, renpy.random.choice([_("Flattery will get you everywhere."), _("Good answer. You're not bad yourself.")]))
            Change_Status(girl, "Love", 4)
            Change_Status(girl, "Inbt", 2)
        elif _choice == "new":
            set_scene_expression(girl, "smile")
            Say_Line(girl, renpy.random.choice([_("New things? Like what? ...Actually, I'm curious."), _("Always room to grow. I like that attitude.")]))
            Change_Status(girl, "Inbt", 5)
        else:
            set_scene_expression(girl, "angry")
            Say_Line(girl, renpy.random.choice([_("Practice?! ...I'll show you practice."), _("Wow. That's the last time I ask for your opinion.")]))
            Change_Status(girl, "Love", -5)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_bed = True

    def cc_girl_asks_think_about(girl, loc, t_index):
        set_scene_expression(girl, "shy")
        Say_Line(girl, _("Do you think about me when I'm not around?"))
        _choice = renpy.display_menu([
            (_("All the time"), "always"),
            (_("Sometimes"), "sometimes"),
            (_("When I'm alone at night"), "night"),
        ])
        if _choice == "always":
            set_scene_expression(girl, "happy")
            Say_Line(girl, renpy.random.choice([_("That's... really sweet. I think about you too."), _("You do? ...I was hoping you'd say that.")]))
            Change_Status(girl, "Love", 6)
        elif _choice == "night":
            set_scene_expression(girl, "sexy")
            Say_Line(girl, renpy.random.choice([_("At night, huh? I wonder what kind of thoughts those are..."), _("Alone at night... thinking about me? That's hot, actually.")]))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Inbt", 5)
        else:
            Say_Line(girl, renpy.random.choice([_("Sometimes? I'll take what I can get."), _("Honest. Not the most romantic, but I appreciate it.")]))
            Change_Status(girl, "Love", 2)
        set_scene_expression(girl, "normal")
        girl._cc_quiz_think = True

    # ============================================================
    # REGISTRATION — Get to Know Her + Girl Quizzes
    # ============================================================

    # Tipo A — Player asks (one-shot, gated by Love/Inbt)
    for _fn, _flag, _love, _inbt in [
        (cc_ask_music, "_cc_asked_music", 50, 0),
        (cc_ask_cooking, "_cc_asked_cooking", 50, 0),
        (cc_ask_morning_night, "_cc_asked_morning", 50, 0),
        (cc_ask_bored, "_cc_asked_bored", 50, 0),
        (cc_ask_fav_place, "_cc_asked_fav_place", 50, 0),
        (cc_ask_perfect_date, "_cc_asked_date", 150, 0),
        (cc_ask_family, "_cc_asked_family", 150, 0),
        (cc_ask_pet_peeve, "_cc_asked_peeve", 150, 0),
        (cc_ask_trust, "_cc_asked_trust", 150, 0),
        (cc_ask_regret, "_cc_asked_regret", 150, 0),
        (cc_ask_guilty_pleasure, "_cc_asked_guilty", 300, 200),
        (cc_ask_adventurous, "_cc_asked_adventurous", 300, 200),
        (cc_ask_boldest, "_cc_asked_boldest", 300, 200),
        (cc_ask_jealous, "_cc_asked_jealous", 300, 200),
        (cc_ask_sharing, "_cc_asked_sharing", 300, 200),
        (cc_ask_hard_limits, "_cc_asked_limits", 300, 200),
        (cc_ask_turn_on, "_cc_asked_turnon", 500, 400),
        (cc_ask_control, "_cc_asked_control", 500, 400),
        (cc_ask_fantasy, "_cc_asked_fantasy", 500, 400),
        (cc_ask_want_to_try, "_cc_asked_try", 500, 400),
    ]:
        register_chitchat(
            "global", _fn,
            condition=lambda g, loc, t, _f=_flag, _l=_love, _i=_inbt: (
                not getattr(g, _f, False)
                and getattr(g, "Love", 0) >= _l
                and getattr(g, "Inbt", 0) >= _i
            ),
            weight=3,
        )

    # Tipo B — Girl quizzes player (one-shot, gated, has menu)
    for _fn, _flag, _love, _inbt in [
        (cc_girl_asks_type, "_cc_quiz_type", 100, 0),
        (cc_girl_asks_pretty, "_cc_quiz_pretty", 100, 0),
        (cc_girl_asks_first_notice, "_cc_quiz_notice", 100, 0),
        (cc_girl_asks_dating, "_cc_quiz_jealous", 250, 0),
        (cc_girl_asks_boring, "_cc_quiz_boring", 250, 0),
        (cc_girl_asks_spend_time, "_cc_quiz_time", 250, 0),
        (cc_girl_asks_crazy, "_cc_quiz_crazy", 400, 300),
        (cc_girl_asks_good_in_bed, "_cc_quiz_bed", 400, 300),
        (cc_girl_asks_think_about, "_cc_quiz_think", 400, 300),
    ]:
        register_chitchat(
            "global", _fn,
            condition=lambda g, loc, t, _f=_flag, _l=_love, _i=_inbt: (
                not getattr(g, _f, False)
                and getattr(g, "Love", 0) >= _l
                and getattr(g, "Inbt", 0) >= _i
            ),
            weight=4,
        )

    # Mark quiz topics as having menus (disable in phone mode)
    for _fn in (
        cc_girl_asks_type, cc_girl_asks_pretty, cc_girl_asks_first_notice,
        cc_girl_asks_dating, cc_girl_asks_boring, cc_girl_asks_spend_time,
        cc_girl_asks_crazy, cc_girl_asks_good_in_bed, cc_girl_asks_think_about,
    ):
        _CHITCHAT_HAS_MENU.add(_fn)

    # Mark topics with interactive menus (unsafe for phone mode)
    for _fn in (
        chitchat_first_introduction,
        chitchat_what_do_you_do,
        chitchat_player_hobby,
        chitchat_do_you_work_out,
        chitchat_have_a_girlfriend,
        chitchat_first_impression,
        chitchat_eat_together,
        chitchat_you_look_different,
        chitchat_talked_to_others,
        chitchat_ask_player_fav,
        chitchat_ask_what_about_tits,
        chitchat_ask_what_about_ass,
    ):
        _CHITCHAT_HAS_MENU.add(_fn)

    # ==========================================================
    # NTW-SPECIFIC CHITCHATS
    # ==========================================================

    # ----------------------------------------------------------
    # NTW asks about girls in class (one-shot, menu)
    # ----------------------------------------------------------
    def chitchat_ntw_girls_in_class(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("So... noticed any cute girls around here?"))

        _has_rogue = any(g.gid == "rogue" for g in store.ALL_GIRLS)

        _choices = []
        _choices.append((_("Gwen is pretty cool, actually."), "gwen"))
        if _has_rogue:
            _choices.append((_("Rogue has this mysterious thing going on..."), "rogue"))
        _choices.append((_("There's this cute girl with short hair... petite, looks tough."), "ntw_hint"))
        _choices.append((_("Honestly? I've only been noticing you."), "player"))

        result = renpy.display_menu(_choices)

        if result == "gwen":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Gwen? Yeah... she's got something."))
            renpy.pause(0.3)
            Say_Line(girl, _("Good eye."))
            set_scene_expression(girl, "normal")
            Change_Status(girl, "Love", 5)

        elif result == "rogue":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Rogue... yeah. She's interesting."))
            renpy.pause(0.3)
            Say_Line(girl, _("The quiet ones usually are."))
            set_scene_expression(girl, "normal")
            Change_Status(girl, "Love", 5)

        elif result == "ntw_hint":
            set_scene_expression(girl, "surprise")
            Say_Line(girl, _("...what?"))
            renpy.pause(0.5)
            set_scene_expression(girl, "shy")
            Say_Line(girl, _("...are you describing me right now?"))
            renpy.pause(0.3)
            set_scene_expression(girl, "angry")
            Say_Line(girl, _("...you're an idiot."))
            set_scene_expression(girl, "normal")
            Change_Status(girl, "Obed", 8)
            Change_Status(girl, "Inbt", 5)

        elif result == "player":
            set_scene_expression(girl, "surprise")
            Say_Line(girl, _("..."))
            renpy.pause(0.5)
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Whatever."))
            Change_Status(girl, "Love", 8)
            Change_Status(girl, "Inbt", 5)

        girl.set_flag("_cc_ntw_girls", True)

    register_chitchat(
        "ntw", chitchat_ntw_girls_in_class,
        condition=lambda g, loc, t: (
            not getattr(g, "_cc_ntw_girls", False)
            and getattr(g, "Love", 0) >= 80
        ),
        weight=5,
    )
    _CHITCHAT_HAS_MENU.add(chitchat_ntw_girls_in_class)

    # ----------------------------------------------------------
    # NTW comfortable silence (repeatable, no menu)
    # ----------------------------------------------------------
    def chitchat_ntw_silence(girl, loc, t_index):
        _openers = [
            _("..."),
            _("You don't have to talk, you know."),
            _("Quiet is fine."),
        ]
        set_scene_expression(girl, "normal")
        Say_Line(girl, _tl(renpy.random.choice(_openers)))
        renpy.pause(0.5)

        _followups = [
            _("...this is the only kind of company I don't hate."),
            _("Most people ruin silence. You don't."),
            _("...not bad."),
        ]
        Say_Line(girl, _tl(renpy.random.choice(_followups)))
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 3)

    register_chitchat("ntw", chitchat_ntw_silence, weight=3)

    # ----------------------------------------------------------
    # NTW earbuds / music (one-shot, menu)
    # ----------------------------------------------------------
    def chitchat_ntw_earbuds(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("..."))
        renpy.say(None, _("She has one earbud in, barely acknowledging you."))

        _choices = [
            (_("What are you listening to?"), "ask"),
            (_("(Say nothing, just sit nearby.)"), "silent"),
        ]
        result = renpy.display_menu(_choices)

        if result == "ask":
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("Noise."))
            renpy.pause(0.3)
            Say_Line(girl, _("...industrial metal. You wouldn't like it."))
            renpy.pause(0.3)
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("...or maybe you would. I don't care either way."))
            Change_Status(girl, "Love", 3)
            Change_Status(girl, "Obed", 2)
        else:
            renpy.pause(0.8)
            set_scene_expression(girl, "normal")
            Say_Line(girl, _("...hm."))
            renpy.pause(0.5)
            Say_Line(girl, _("You're alright."))
            Change_Status(girl, "Love", 5)

        girl.set_flag("_cc_ntw_earbuds", True)

    register_chitchat(
        "ntw", chitchat_ntw_earbuds,
        condition=lambda g, loc, t: not getattr(g, "_cc_ntw_earbuds", False),
        weight=4,
    )
    _CHITCHAT_HAS_MENU.add(chitchat_ntw_earbuds)

    # ----------------------------------------------------------
    # NTW campus observation (repeatable, no menu)
    # ----------------------------------------------------------
    def chitchat_ntw_campus_boring(girl, loc, t_index):
        _lines = [
            (_("Everyone here acts like they're in a movie. It's exhausting."), _("This place runs on caffeine and fake smiles.")),
            (_("Campus food is trash."), _("At least it's consistent.")),
            (_("Half these people won't last the semester."), _("Natural selection.")),
            (_("I've been here a while and still don't know most people's names."), _("...I don't plan to.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    register_chitchat("ntw", chitchat_ntw_campus_boring, weight=2)

    # ----------------------------------------------------------
    # NTW independence / don't need friends (one-shot, no menu)
    # ----------------------------------------------------------
    def chitchat_ntw_independence(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("I don't need a group. I had one once. Lots of rules, lots of 6 AM drills."))
        renpy.pause(0.3)
        Say_Line(girl, _("People slow you down. They expect things."))
        renpy.pause(0.3)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("...you're the exception so far. Don't ruin it."))
        Change_Status(girl, "Love", 5)
        Change_Status(girl, "Obed", 3)
        girl.set_flag("_cc_ntw_independence", True)

    register_chitchat(
        "ntw", chitchat_ntw_independence,
        condition=lambda g, loc, t: (
            not getattr(g, "_cc_ntw_independence", False)
            and getattr(g, "Love", 0) >= 150
        ),
        weight=4,
    )

    # ----------------------------------------------------------
    # NTW notices player is persistent (one-shot, high Love gate)
    # ----------------------------------------------------------
    def chitchat_ntw_persistent(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("You keep showing up."))
        renpy.pause(0.3)
        Say_Line(girl, _("Most people stop trying after the first week."))
        renpy.pause(0.5)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("...I guess you're stubborn."))
        renpy.pause(0.3)
        Say_Line(girl, _("...I don't hate stubborn."))
        Change_Status(girl, "Love", 8)
        girl.set_flag("_cc_ntw_persistent", True)

    register_chitchat(
        "ntw", chitchat_ntw_persistent,
        condition=lambda g, loc, t: (
            not getattr(g, "_cc_ntw_persistent", False)
            and getattr(g, "Love", 0) >= 300
        ),
        weight=5,
    )

    # ----------------------------------------------------------
    # NTW hints at girl preference (one-shot, mid Love)
    # ----------------------------------------------------------
    def chitchat_ntw_girl_preference(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("You ever notice how girls smell better than guys?"))
        renpy.pause(0.3)
        Say_Line(girl, _("Like... always. No exceptions."))
        renpy.pause(0.5)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("...don't look at me like that. It's just a fact."))
        Change_Status(girl, "Love", 3)
        Change_Status(girl, "Obed", 2)
        girl.set_flag("_cc_ntw_girl_pref", True)

    register_chitchat(
        "ntw", chitchat_ntw_girl_preference,
        condition=lambda g, loc, t: (
            not getattr(g, "_cc_ntw_girl_pref", False)
            and getattr(g, "Love", 0) >= 200
        ),
        weight=4,
    )

    # ----------------------------------------------------------
    # NTW personal space rant (repeatable, no menu)
    # ----------------------------------------------------------
    def chitchat_ntw_personal_space(girl, loc, t_index):
        _lines = [
            (_("Some guy tried to put his arm around me at the gym."), _("He won't try again.")),
            (_("People here stand way too close when they talk."), _("I don't get it. Back up.")),
            (_("Someone bumped into me in the hallway and didn't apologize."), _("I made sure they noticed.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "angry")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _pick[1])
        Change_Status(girl, "Inbt", 2)

    register_chitchat("ntw", chitchat_ntw_personal_space, weight=2)

    # ----------------------------------------------------------
    # Bisexual reveal — she casually drops that she likes both
    # One-shot, requires Love >= 150, triggers discovery banner
    # ----------------------------------------------------------
    def chitchat_bisexual_reveal(girl, loc, t_index):
        set_scene_expression(girl, "normal")
        Say_Line(girl, _("That statistics teacher is kinda cute, don't you think?"))
        renpy.pause(0.3)
        set_scene_expression(girl, "smirk")
        Say_Line(girl, _("What? I play for both teams. No big deal."))
        renpy.pause(0.3)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _("Guys, girls... a hot person is a hot person."))
        Change_Status(girl, "Love", 3)
        girl.discover("discovered_trait_bisexual")

    register_chitchat(
        "global", chitchat_bisexual_reveal,
        condition=lambda g, loc, t: (
            hasattr(g, "has_trait") and g.has_trait("bisexual")
            and not g.flags.get("discovered_trait_bisexual", False)
            and getattr(g, "Love", 0) >= 150
        ),
        weight=5,
        student=True,
    )

    # ----------------------------------------------------------
    # Tenny: study rambling (core personality)
    # ----------------------------------------------------------
    def chitchat_tenny_study(girl, loc, t_index):
        _openers = [
            (_("Did you know the library has a quiet room behind the archives?"), _("Best-kept secret on campus. You're welcome.")),
            (_("I made a study schedule for the whole semester on day one."), _("Already ahead of it, obviously.")),
            (_("I highlight in four colors. Each one means something specific."), _("Pink is 'this will be on the exam'. I'm rarely wrong.")),
            (_("My notes have a table of contents."), _("Don't look at me like that. Organization is a skill.")),
        ]
        _pick = renpy.random.choice(_openers)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "sexy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    register_chitchat("tenny", chitchat_tenny_study, weight=3)

    # ----------------------------------------------------------
    # Tenny: grade competitiveness
    # ----------------------------------------------------------
    def chitchat_tenny_grades(girl, loc, t_index):
        _lines = [
            (_("Someone asked me to 'just relax' about grades."), _("Relax? I have a GPA to maintain.")),
            (_("I got a 98 on the last test."), _("I'm still looking for those two points I lost.")),
            (_("The curve on that exam saved half the class."), _("I didn't need it, but you're welcome for raising the average.")),
            (_("A guy in my class copies my notes every week."), _("At least someone appreciates good handwriting.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "angry")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Obed", 1)

    register_chitchat("tenny", chitchat_tenny_grades, weight=2)

    # ----------------------------------------------------------
    # Tenny: exam anxiety (classroom only)
    # ----------------------------------------------------------
    def chitchat_tenny_exam_anxiety(girl, loc, t_index):
        _lines = [
            (_("I have THREE exams next week. THREE."), _("I've already made 47 flashcards. It's not enough.")),
            (_("I dreamed about failing a test last night."), _("I woke up and studied for two hours. At 3 AM.")),
            (_("The professor said 'this won't be on the exam.'"), _("I'm studying it anyway. Professors LIE.")),
            (_("I calculated the exact minimum grade I need on the final."), _("It's a 94. So basically, I need to be perfect. As usual.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "scared")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "angry")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Obed", 1)

    register_chitchat("tenny", chitchat_tenny_exam_anxiety,
        condition=lambda g, loc, t: loc == "classroom", weight=2)

    # ----------------------------------------------------------
    # Tenny: professor observation (classroom only)
    # ----------------------------------------------------------
    def chitchat_tenny_professor_observation(girl, loc, t_index):
        _lines = [
            (_("Professor Daniels always brings that same coffee mug."), _("I timed it once. He takes a sip every 4 minutes and 12 seconds.")),
            (_("The TA grades way harder than the professor."), _("I got a 96 once and she wrote 'good effort' like it was a participation trophy.")),
            (_("Professor Hart tells the worst jokes before every lecture."), _("...I laugh every time. They're so bad they loop back to being funny.")),
            (_("The new professor actually explains things clearly."), _("I almost forgot what it's like to understand something on the first try.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "normal")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)

    register_chitchat("tenny", chitchat_tenny_professor_observation,
        condition=lambda g, loc, t: loc == "classroom", weight=2)

    # ----------------------------------------------------------
    # Tenny: study spot (classroom only)
    # ----------------------------------------------------------
    def chitchat_tenny_study_spot(girl, loc, t_index):
        _lines = [
            (_("I always sit in the front row. Third seat from the left."), _("If someone takes MY seat, my whole day is ruined.")),
            (_("I color-code all my notes. Blue for theory, red for formulas."), _("Green for 'the professor said this exact phrase will be on the test.'")),
            (_("Someone asked to borrow my notes last week."), _("I made them a COPY. Nobody touches the originals.")),
            (_("I have a snack drawer under this desk. Don't tell anyone."), _("It's all energy bars and gummy bears. Brain fuel.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "shy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    register_chitchat("tenny", chitchat_tenny_study_spot,
        condition=lambda g, loc, t: loc == "classroom", weight=2)

    # ----------------------------------------------------------
    # Tenny: classmate drama (classroom only)
    # ----------------------------------------------------------
    def chitchat_tenny_classmate_drama(girl, loc, t_index):
        _lines = [
            (_("Someone in this class plagiarized their entire paper."), _("The professor read both versions out loud. WITHOUT naming anyone. The silence was deafening.")),
            (_("My group project partner hasn't answered a single message in two weeks."), _("I'm doing the whole thing myself. AGAIN. And I'll still put their name on it because I'm too nice.")),
            (_("The grade curve this semester is brutal."), _("Half the class failed the midterm. I got an 89 and I'm in the top five. That's terrifying.")),
            (_("There's a study group that meets on Thursdays."), _("They spend more time arguing about pizza toppings than actually studying. I went ONCE.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "surprised")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "angry")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Obed", 1)

    register_chitchat("tenny", chitchat_tenny_classmate_drama,
        condition=lambda g, loc, t: loc == "classroom", weight=1)

    # ----------------------------------------------------------
    # Tenny: guilty pleasures
    # ----------------------------------------------------------
    def chitchat_tenny_guilty_pleasure(girl, loc, t_index):
        _lines = [
            (_("If you tell ANYONE I watch reality dating shows, I will end you."), _("Academically. I will end you ACADEMICALLY.")),
            (_("I may or may not have a playlist called 'Study Music.'"), _("It's entirely pop songs. Not a single classical track.")),
            (_("I read romance novels. For the PLOT."), _("The plot is very... detailed. Anatomically accurate, even.")),
            (_("Sometimes I eat instant ramen for dinner three days in a row."), _("My nutritional spreadsheet has a LOT of red cells this month.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "shy")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 2)

    register_chitchat("tenny", chitchat_tenny_guilty_pleasure, weight=1)

    # ----------------------------------------------------------
    # Tenny: competitive streak
    # ----------------------------------------------------------
    def chitchat_tenny_competitive(girl, loc, t_index):
        _lines = [
            (_("I don't NEED to be the best at everything."), _("I just AM. There's a difference.")),
            (_("Second place is just first loser."), _("That's not toxic. That's motivation.")),
            (_("Someone beat me on the last quiz by ONE point."), _("I've been plotting my comeback since Tuesday.")),
            (_("My classmate said she studies 'casually.'"), _("Casually? I don't even breathe casually during exam week.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "angry")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "sexy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Inbt", 1)

    register_chitchat("tenny", chitchat_tenny_competitive, weight=2)

    # ----------------------------------------------------------
    # Tenny: martial arts / gym (gym only)
    # ----------------------------------------------------------
    def chitchat_tenny_martial_arts(girl, loc, t_index):
        _lines = [
            (_("Kickboxing is basically math."), _("Angle, force, timing. I'm very good at math.")),
            (_("People always underestimate the small girl at the gym."), _("Their surprise when I outlift them is deeply satisfying.")),
            (_("I started martial arts because the dojo was next to the library."), _("Stayed because punching things is an excellent stress release.")),
            (_("My trainer says I have 'surprisingly aggressive energy.'"), _("I channeled my exam rage into a roundhouse kick. He was impressed.")),
            (_("I did karate all through my teens. I got pretty far up the belts."), _("My cousin stopped picking fights with me right around then. Coincidence, I'm sure.")),
        ]
        _pick = renpy.random.choice(_lines)
        set_scene_expression(girl, "happy")
        Say_Line(girl, _pick[0])
        renpy.pause(0.3)
        set_scene_expression(girl, "sexy")
        Say_Line(girl, _pick[1])
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", 1)
        Change_Status(girl, "Obed", 1)

    register_chitchat("tenny", chitchat_tenny_martial_arts,
        condition=lambda g, loc, t: loc == "gym", weight=1)

    # ==========================================================
    # PERSONALITY TOPICS: the person behind the girl
    # ==========================================================
    # Author canon, docs/Personality.md (2026-09-19). Small references, never exposition: a player who does not know
    # where she comes from sees a girl with a past, a fan recognizes the wink. Nobody ever says she has powers.
    # One topic = a pool of pairs (she says the first line, then the second), one face per line, a small Love gain.
    #   pairs:       [(line, line), ...] or {trait: [...], "_default": [...]}: the first trait she has picks the pool
    #                (a lesbian does not tell the story of the boy she liked the same way)
    #   partner:     the lines are about her partner: %(pl)s / %(pp)s / %(Pp)s, filled AFTER the translation
    #                (interactions.rpy _format_partner_line); the topic's condition asks for her NPC partner
    #   canon_pairs: more pairs, only with the partner her story gives her (npc_partner.rpy _NPC_CANON_NAMES)
    # chitchat_<gid>_<topic> below are named one-liners on purpose: the topic the chitchat label picked sits in a
    # store variable, so a save pickles it BY NAME. Tenny speaks with her confident voice here (she stutters only
    # about the pregnancy).
    _PERSONA_TOPICS = {
        # ---- Gwen: an artist since she was a kid (a sketchbook nobody sees), goth, a reality show years ago told as ordinary
        #      teenage memories (camp, island, cameras, eliminations, alliances), love born in a competition
        "gwen_art": {"faces": ("thinking", "smirk"), "love": 2, "pairs": [
            (_("I've been drawing since I was a kid."), _("It's one of the only things that actually shuts my brain up.")),
            (_("I used to sketch people when I got bored."), _("Relax, you're not in there. ...Yet.")),
            (_("It doesn't have to be pretty."), _("Sometimes I just need to get an idea out of my head and onto paper before it eats me alive.")),
            (_("I learned to draw people because it was easier than talking to them."), _("Turns out it also teaches you to actually look at them. Nobody warns you about that part.")),
            (_("I still have some drawings from back then."), _("Most of them should stay buried. A couple are the best thing I've ever made.")),
            (_("No, you can't see my sketchbook."), _("Nobody sees the sketchbook. That's the whole point of the sketchbook.")),
        ]},
        "gwen_show": {"faces": ("bemused", "smirk"), "love": 1, "pairs": [
            (_("I once spent a whole summer at a camp full of teenagers, with cameras on me the entire time."), _("After that, college feels like a spa.")),
            (_("You learn a lot about a person when you're forced to compete against them."), _("Mostly how fast they'd push you off a cliff for a trophy. Figuratively. Mostly.")),
            (_("I've had to team up with people I couldn't stand."), _("You'd be amazed what you can tolerate when the alternative is getting sent home.")),
            (_("I've been voted out of things for way dumber reasons than a bad grade."), _("So no, this exam isn't keeping me up at night.")),
            (_("Try spending weeks on an island with people you barely know."), _("The food fought back, the cabins leaked, and the guy in charge thought it was all hilarious.")),
            (_("I learned not to trust someone just because they're nice in front of a camera."), _("The friendliest face in the room is usually the one planning your elimination.")),
        ]},
        "gwen_cameras": {"faces": ("serious", "bemused"), "love": 1, "pairs": {
            "camera_lover": [
                (_("Everyone assumes I hate cameras after everything that happened back then."), _("Honestly? I got used to them. Maybe a little too used to them.")),
                (_("I spent weeks talking to a camera in a tiny booth once."), _("Some girls get stage fright. I got a habit.")),
            ],
            "_default": [
                (_("I had a bad experience with cameras once."), _("I'd rather not get into it. Seriously.")),
                (_("I can always tell when someone's putting on a show for other people."), _("I've seen professionals. Most people on this campus are amateurs.")),
                (_("Sharing a room with a bunch of strangers is worse than it sounds."), _("Trust me. I did it with a leaky roof and a raccoon problem.")),
                (_("I went weeks once with basically zero privacy."), _("Now I lock my door just because I can.")),
            ],
        }},
        "gwen_ex": {"faces": ("thinking", "bemused"), "love": 2, "pairs": {
            "lesbian": [
                (_("I dated someone I met during a competition once."), _("Terrible idea. Dating someone you're also trying to beat complicates things a little.")),
                (_("A guy once wrote me a song on his guitar."), _("Sweet. Wrong audience, as it turned out. VERY wrong audience.")),
                (_("My best friend and I stopped talking over someone we both liked."), _("I'm not proud of my part in it. Neither of us came out of it looking good.")),
                (_("Let's just say my love life used to be... complicated."), _("Love triangles are a lot less fun when you're one of the corners.")),
            ],
            "_default": [
                (_("I dated someone I met during a competition once."), _("Terrible idea. Dating someone you're also trying to beat complicates things a little.")),
                (_("There was this guy who played guitar and wrote me a song."), _("Sweet for about a week. Then it got weird. Then it got REALLY weird.")),
                (_("My best friend and I stopped talking over a guy."), _("I'm not proud of my part in it. I'm not proud of his either.")),
                (_("Let's just say my love life used to be... complicated."), _("Love triangles are a lot less fun when you're one of the corners.")),
            ],
        }},
        "gwen_goth": {"faces": ("smirk", "bemused"), "love": 1, "pairs": [
            (_("People keep asking when my 'dark phase' is going to end."), _("It's been a very long phase. I'm very committed to it.")),
            (_("I'd rather stay in and draw than go to a party full of people pretending to have fun."), _("Invite me when the party has a quiet corner and a decent pen.")),
            (_("I own exactly one piece of clothing that isn't black."), _("It was a gift. It lives in the back of the closet, where it belongs.")),
            (_("I'm used to living with people who are nothing like me."), _("Put me in a cabin with a jock, a princess and a guy who eats everything. I'll survive. I have.")),
        ]},
        # ---- Rogue: the South (accent, food, horses), raised by her AUNT (her mother: complicated), a chosen family in a big
        #      house full of people, careful with touch (gloves), a boy she liked a lot. Never says she has powers.
        "rogue_home": {"faces": ("smile", "bemused"), "love": 2, "pairs": [
            (_("I grew up down South, sugar."), _("You learn a few things real early down there. Mostly how to handle the heat and folks who talk too much.")),
            (_("My aunt practically raised me."), _("That woman could fix a fence, bake a pie and put a grown man in his place, all before lunch.")),
            (_("I miss some things from home."), _("Mostly the food. Nobody up here knows what real cornbread is supposed to taste like.")),
            (_("Don't mess with a southern girl, darlin'."), _("We smile real sweet right up until we don't.")),
            (_("I used to ride every mornin' back home."), _("Nothin' clears your head like a good horse and an open field. This campus has neither.")),
            (_("My aunt called this mornin'."), _("Asked if I'm eatin' right, sleepin' right and goin' to church. Two outta three, sugar.")),
        ]},
        "rogue_family": {"faces": ("thinking", "smile"), "love": 2, "pairs": [
            (_("My family's... complicated."), _("Let's just leave it at that for now, sugar.")),
            (_("I spent a few years livin' with a bunch of folks who ended up bein' my family."), _("We weren't kin. Back then that didn't make a lick of difference.")),
            (_("That big old house was always full of people."), _("You never got a minute of privacy. I miss it more than I'd ever tell 'em.")),
            (_("I learned early that family don't always mean blood."), _("Sometimes it's just the folks who show up when it counts.")),
            (_("There's a girl I grew up with in that house."), _("We ain't related, but she's my sister in every way that counts. She'd tease me about you for a month.")),
            (_("I've lived with folks a whole lot stranger than anybody on this campus."), _("Trust me, sugar. Y'all are downright normal.")),
        ]},
        "rogue_touch": {"faces": ("shy", "smile"), "love": 2, "pairs": [
            (_("I went through a phase where I couldn't touch folks without worryin' what might happen."), _("Long story. Took me years to feel easy about it.")),
            (_("You got no idea how hard it is to keep your distance when everybody wants a hug."), _("I got real good at the side-step. Olympic level.")),
            (_("People always ask about my gloves."), _("Habit, mostly. I wore 'em so long my hands feel naked without 'em.")),
            (_("I spent years learnin' to keep a lid on certain things about me."), _("Some days the lid still rattles.")),
            (_("There was a time I figured somethin' was real wrong with me."), _("Took a long while 'fore I felt anywhere near normal.")),
            (_("I don't do hospitals, sugar."), _("White rooms, cold hands, folks pokin' at you. No, thank you.")),
        ]},
        "rogue_past": {"faces": ("sad", "smile"), "love": 2, "pairs": {
            "lesbian": [
                (_("There was a boy once. Charmin' as sin, and I cared about him a whole lot."), _("Just never the way he wanted. Took us both a long time to see it.")),
                (_("He used to shuffle a deck of cards while he talked to me."), _("Drove me crazy. The good kind of crazy and the bad kind.")),
                (_("When I was younger, I fell in with a woman I figured for a second mama."), _("She wasn't. Took me a long time to see it, and even longer to quit missin' her.")),
                (_("I spent a good chunk of my teens away from home."), _("Wasn't exactly the easiest stretch of my life. I came out the other side, though.")),
            ],
            "_default": [
                (_("I had somethin' complicated with a boy I liked a whole lot."), _("Likin' somebody don't mean it's gonna work. Took me a long time to learn that.")),
                (_("He used to shuffle a deck of cards while he talked to me."), _("Drove me crazy. The good kind of crazy and the bad kind.")),
                (_("Him and me had a real complicated history."), _("Close enough to hurt, never close enough to hold. That about sums it up.")),
                (_("When I was younger, I fell in with a woman I figured for a second mama."), _("She wasn't. Took me a long time to see it, and even longer to quit missin' her.")),
                (_("I spent a good chunk of my teens away from home."), _("Wasn't exactly the easiest stretch of my life. I came out the other side, though.")),
            ],
        }},
        "rogue_training": {"faces": ("serious", "smirk"), "love": 1, "pairs": [
            (_("I learned to fight years back, from folks who didn't believe in goin' easy."), _("Now I just come here to remind my body it still remembers.")),
            (_("Somebody told me a long time ago that you train so you never have to find out."), _("I still hear it every time I think about skippin' a session.")),
            (_("We had a trainin' room back at that old house."), _("Folks called it the danger room, and they weren't kiddin'.")),
            (_("I can throw a punch, sugar."), _("I just hope I never have to show you.")),
        ]},
        # ---- NTW: dry, sarcastic, unimpressed. Years of daily training with a group (instructors, "missions"), tech,
        #      an "explosive temper", fragile things, one loudmouth she once had to work with. Her partner only when she has one.
        "ntw_training": {"faces": ("serious", "smirk"), "love": 1, "pairs": [
            (_("I spent a few years training every day."), _("You pick up habits. Like checking every exit when I walk into a room.")),
            (_("I learned to fight before I learned to relax."), _("Still working on the second one.")),
            (_("My training wasn't exactly the kind of extracurricular parents recommend."), _("No certificate. Just bruises and one very disappointed instructor.")),
            (_("I've had instructors way scarier than any professor here."), _("One was seven feet tall and gave speeches about honor. Every. Single. Day.")),
            (_("I've been on a couple of... group projects."), _("The kind where things blow up if one person doesn't follow the plan.")),
            (_("Short hair is practical."), _("You'd be amazed how often long hair gets grabbed in a fight.")),
        ]},
        "ntw_temper": {"faces": ("annoyed", "smirk"), "love": 1, "pairs": [
            (_("I've got a bit of an explosive temper."), _("Figuratively. ...Mostly.")),
            (_("Rule one: keep fragile things away from me."), _("I have a bad track record with them.")),
            (_("I learned to control my anger."), _("The walls are grateful.")),
            (_("No, I'm not going to explode."), _("Probably.")),
            (_("There was a time everything I touched ended up broken."), _("I'm better now. Ask the vending machine. Actually, don't.")),
            (_("Let's just say I had an... explosive adolescence."), _("Some of the scorch marks are probably still there.")),
        ]},
        "ntw_tech": {"faces": ("neutral", "smirk"), "love": 1, "pairs": [
            (_("I build my own computers."), _("Store-bought ones don't survive me. Long story.")),
            (_("I don't buy cheap electronics."), _("They fry. Around me, specifically. Don't ask.")),
            (_("Someone in my building had 'password' as their wifi password."), _("Had. I fixed it. They'll never know. You're welcome, humanity.")),
            (_("I fixed the campus printer last week."), _("Nobody asked. It just offended me.")),
            (_("I had some problems with electricity when I was younger."), _("Nothing I want to repeat.")),
        ]},
        "ntw_loudmouth": {"faces": ("annoyed", "bemused"), "love": 1, "pairs": [
            (_("I once had to work with a guy who couldn't shut up for five minutes."), _("I'd have preferred another fight.")),
            (_("Trust me. I've met people way more annoying than you."), _("You're not even top ten. Don't make it a goal.")),
            (_("I once had to babysit a grown man who acted like a toddler."), _("He talked to people who weren't even there. Don't recommend it.")),
            (_("I was on a job once that should've taken ten minutes."), _("If one person had followed the plan. One. He did not.")),
            (_("Somebody once told me I had the coolest name ever."), _("Then he didn't stop talking for two hours. Don't become that guy.")),
        ]},
        "ntw_partner": {"faces": ("neutral", "smirk"), "love": 1, "partner": True, "pairs": [
            (_("My %(pl)s is the only person who can talk me into being social."), _("I still don't know how %(pp)s does it. Witchcraft, probably.")),
            (_("My %(pl)s is way more optimistic than me."), _("I don't know how %(pp)s manages it. It's exhausting to watch.")),
            (_("My %(pl)s is used to the way I am."), _("That's rarer than you'd think.")),
            (_("My %(pl)s says I need to smile more."), _("I disagree.")),
        ], "canon_pairs": [
            (_("We met during a really weird time of my life."), _("%(Pp)s said hi to me like we were already friends. Turns out %(pp)s was right. Annoying.")),
        ]},
        # ---- Tenny (canon 2026-09-19): raised by her parents; grandpa = plumber, the old RV summers with her cousin, tools,
        #      his taste in women; beyond the syllabus, astronomy, ancient history, occult / runes, a rebel ex
        "tenny_grandpa": {"faces": ("happy", "bemused"), "love": 2, "pairs": [
            (_("My grandpa was a plumber for forty years."), _("He always said it was a lot harder than people think. After watching him fix a burst pipe at 2 AM, I believe him.")),
            (_("I spent basically every summer of my childhood in my grandpa's old RV."), _("Me, him and my cousin. Weeks at a time. You learn a LOT about a person in a space that small.")),
            (_("My grandpa taught me how to use tools. He can fix practically anything."), _("I can replace a faucet in fifteen minutes. It's the least academic thing about me and I love it.")),
            (_("When I was a kid, my grandpa took us camping all the time."), _("I planned the routes. My cousin just showed up and found a way to turn it into a disaster.")),
            (_("My parents were the sensible ones. Bedtime, vegetables, homework first."), _("Grandpa was the one who said 'pack a bag, kiddo' and drove us across three states. I needed both.")),
            (_("My grandpa has always had... unusual taste in women."), _("I've met a few of his exes. One of them I'm still not convinced was entirely human. I'm only mostly joking.")),
        ]},
        "tenny_curiosity": {"faces": ("thinking", "happy"), "love": 1, "pairs": [
            (_("I've always liked studying things that weren't on the syllabus."), _("Last night it was the history of map making. It has NOTHING to do with my major. It was great.")),
            (_("Astronomy always gets to me."), _("It's hard to look up at the sky and not want to know what's out there. Some of it would surprise you.")),
            (_("I used to look up strange things on my laptop just because I got curious."), _("Lights nobody could explain, ships that vanished, that kind of thing. I still have the bookmarks. There are a lot of bookmarks.")),
            (_("Ancient history gets so much better once you dig into the details."), _("There are writing systems nobody has cracked yet. It drives me insane. In a good way.")),
            (_("I once stayed up all night researching something that wasn't even in my field."), _("I had an exam the next morning. I still aced it. Do not try this at home.")),
            (_("Right now I have one tab open for class and eleven for a supernova I read about."), _("The supernova is winning.")),
            (_("It bothers me when people treat a hypothesis like a fact."), _("Do the research FIRST. Then have the opinion. It is not that hard.")),
            (_("I don't like waiting for someone to explain things to me."), _("So I teach myself. It's slower at first, and then it's much, much faster.")),
        ]},
        "tenny_occult": {"faces": ("thinking", "smirk"), "love": 1, "pairs": [
            (_("I got into the occult out of pure academic curiosity."), _("I ended up taking it more seriously than I planned. Don't look at me like that.")),
            (_("Old books are fascinating."), _("Especially once you notice that some of what's in them isn't as fictional as it looks.")),
            (_("I went through a phase where I studied symbols and runes."), _("Some of it stuck. If you ever find a weird carving somewhere, call me before you touch it.")),
            (_("You'd be surprised how many different writing systems exist."), _("I can read more of them than I'd ever put on a resume.")),
        ]},
        "tenny_ex": {"faces": ("thinking", "bemused"), "love": 2, "pairs": {
            "lesbian": [
                (_("I dated a guy in high school. A complete rebel."), _("Hated school, hated rules. I liked him, in a way. It just took me a while to figure out which way.")),
                (_("My ex thought studying was a waste of time."), _("I thought he was wasting his. We were both a little bit right and completely incompatible.")),
            ],
            "_default": [
                (_("I dated a guy in high school who was a complete rebel."), _("Hated school, hated rules, hated homework. I liked him anyway. It was never going to work.")),
                (_("My ex thought studying was a waste of time."), _("I thought he was wasting his. We were both a little bit right and completely incompatible.")),
            ],
        }},
    }

    def _persona_canon_partner(girl):
        """Her NPC partner is the one her story gives her (_NPC_CANON_NAMES), not someone the game rolled later."""
        if not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
            return False
        _canon = _NPC_CANON_NAMES.get((girl.gid, "female" if girl.get_flag("partner_is_female") else "male"))
        return bool(_canon) and girl.partner_name() == _canon

    def _persona_pairs(girl, key):
        """The pairs she can say for topic `key` right now."""
        _topic = _PERSONA_TOPICS[key]
        _pairs = _topic["pairs"]
        if isinstance(_pairs, dict):
            _pairs = next((_v for _k, _v in _pairs.items() if _k != "_default" and girl.has_trait(_k)), _pairs["_default"])
        if _topic.get("canon_pairs") and _persona_canon_partner(girl):
            _pairs = _pairs + _topic["canon_pairs"]
        return _pairs

    def _persona_topic(girl, key):
        """Plays one personality topic: a random pair of her pool, her two faces, her Love gain."""
        _topic = _PERSONA_TOPICS[key]
        _first, _second = renpy.random.choice(_persona_pairs(girl, key))
        if _topic.get("partner"):
            # translated first, then filled in: "_(..) % x" would never translate
            _first, _second = _format_partner_line(girl, _first), _format_partner_line(girl, _second)
        set_scene_expression(girl, _topic["faces"][0])
        Say_Line(girl, _first)
        renpy.pause(0.3)
        set_scene_expression(girl, _topic["faces"][1])
        Say_Line(girl, _second)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", _topic["love"])
        print("[CHITCHAT] %s %s: %s" % (girl.gid, key, _first[:40]))

    def chitchat_gwen_art(girl, loc, t_index):
        _persona_topic(girl, "gwen_art")

    register_chitchat("gwen", chitchat_gwen_art, weight=2)

    def chitchat_gwen_show(girl, loc, t_index):
        _persona_topic(girl, "gwen_show")

    register_chitchat("gwen", chitchat_gwen_show, weight=2)

    def chitchat_gwen_cameras(girl, loc, t_index):
        _persona_topic(girl, "gwen_cameras")

    register_chitchat("gwen", chitchat_gwen_cameras, weight=1)

    def chitchat_gwen_ex(girl, loc, t_index):
        _persona_topic(girl, "gwen_ex")

    register_chitchat("gwen", chitchat_gwen_ex,
        condition=lambda g, loc, t: getattr(g, "Love", 0) >= 300, weight=1)

    def chitchat_gwen_goth(girl, loc, t_index):
        _persona_topic(girl, "gwen_goth")

    register_chitchat("gwen", chitchat_gwen_goth, weight=1)

    def chitchat_rogue_home(girl, loc, t_index):
        _persona_topic(girl, "rogue_home")

    register_chitchat("rogue", chitchat_rogue_home, weight=2)

    def chitchat_rogue_family(girl, loc, t_index):
        _persona_topic(girl, "rogue_family")

    register_chitchat("rogue", chitchat_rogue_family, weight=2)

    def chitchat_rogue_touch(girl, loc, t_index):
        _persona_topic(girl, "rogue_touch")

    register_chitchat("rogue", chitchat_rogue_touch,
        condition=lambda g, loc, t: getattr(g, "Love", 0) >= 200, weight=1)

    def chitchat_rogue_past(girl, loc, t_index):
        _persona_topic(girl, "rogue_past")

    register_chitchat("rogue", chitchat_rogue_past,
        condition=lambda g, loc, t: getattr(g, "Love", 0) >= 300, weight=1)

    def chitchat_rogue_training(girl, loc, t_index):
        _persona_topic(girl, "rogue_training")

    register_chitchat("rogue", chitchat_rogue_training,
        condition=lambda g, loc, t: loc == "gym", weight=1)

    def chitchat_ntw_training(girl, loc, t_index):
        _persona_topic(girl, "ntw_training")

    register_chitchat("ntw", chitchat_ntw_training, weight=2)

    def chitchat_ntw_temper(girl, loc, t_index):
        _persona_topic(girl, "ntw_temper")

    register_chitchat("ntw", chitchat_ntw_temper, weight=2)

    def chitchat_ntw_tech(girl, loc, t_index):
        _persona_topic(girl, "ntw_tech")

    register_chitchat("ntw", chitchat_ntw_tech, weight=1)

    def chitchat_ntw_loudmouth(girl, loc, t_index):
        _persona_topic(girl, "ntw_loudmouth")

    register_chitchat("ntw", chitchat_ntw_loudmouth, weight=1)

    def chitchat_ntw_partner(girl, loc, t_index):
        _persona_topic(girl, "ntw_partner")

    register_chitchat("ntw", chitchat_ntw_partner,
        condition=lambda g, loc, t: (hasattr(g, "has_npc_partner") and g.has_npc_partner()
                                     and getattr(g, "Player_status", "none") != "dating"), weight=2)

    def chitchat_tenny_grandpa(girl, loc, t_index):
        _persona_topic(girl, "tenny_grandpa")

    register_chitchat("tenny", chitchat_tenny_grandpa, weight=2)

    def chitchat_tenny_curiosity(girl, loc, t_index):
        _persona_topic(girl, "tenny_curiosity")

    register_chitchat("tenny", chitchat_tenny_curiosity, weight=2)

    def chitchat_tenny_occult(girl, loc, t_index):
        _persona_topic(girl, "tenny_occult")

    register_chitchat("tenny", chitchat_tenny_occult, weight=1)

    def chitchat_tenny_ex(girl, loc, t_index):
        _persona_topic(girl, "tenny_ex")

    register_chitchat("tenny", chitchat_tenny_ex,
        condition=lambda g, loc, t: getattr(g, "Love", 0) >= 300, weight=1)

    # ==========================================================
    # PREGNANCY CHITCHAT — Stage 2 (early) and Stage 3 (late)
    # ==========================================================

    # Per-girl line pools for pregnancy stages. A girl with no pool here uses "_default" (girl_pool, pregnancy.rpy).
    _PREG_CHITCHAT_EARLY = {
        "gwen": [
            _("Ugh, I almost threw up in class today. This morning sickness thing is no joke."),
            _("I can't even smell coffee anymore without gagging. Me! The girl who lived on coffee!"),
            _("I ate pickles dipped in ice cream at 2 AM last night. And it was DELICIOUS. What is wrong with me?"),
            _("I've been craving the weirdest combinations. Cheese and chocolate. Together. Don't judge me."),
            _("I fell asleep in the library. Again. My body just shuts down now."),
        ],
        "rogue": [
            _("Sugar, I've been queasy all day. This little one ain't going easy on me."),
            _("I had to leave the cafeteria. The smell of eggs hit me and I nearly lost it right there."),
            _("I woke up wanting barbecue ribs at 6 in the morning. My body has lost its mind."),
            _("I've been eating so much peanut butter I could buy stock in the company."),
            _("I used to train for hours. Now I take the stairs and I'm winded. This is humbling."),
        ],
        "ntw": [
            _("I puked three times before noon. THREE. This kid is already ruining my life."),
            _("If one more person eats fish near me, I'm going to lose it. And by 'it' I mean my lunch."),
            _("I need hot sauce on everything now. EVERYTHING. Even cereal. Don't look at me like that."),
            _("I ate an entire jar of olives in one sitting. I don't even LIKE olives."),
            _("I napped in the gym locker room. On the BENCH. I didn't even care."),
        ],
        "tenny": [
            _("I-I've been feeling really nauseous... I had to skip my morning lecture."),
            _("I read that ginger helps with morning sickness... I've been eating so many ginger candies..."),
            _("I've been craving my mom's apple pie... she mailed me one and I ate half of it in one sitting."),
            _("Is it normal to want to eat chalk? I looked it up and apparently it's a real thing... pica, I think?"),
            _("I keep falling asleep while studying... I set three alarms and still missed one."),
        ],
        "_default": [
            _("The morning sickness is no joke. I barely made it through my first class today."),
            _("Smells get to me now. Someone opened a tuna sandwich next to me and I had to leave the room."),
            _("I keep craving the strangest things. Last night it was pickles and peanut butter. Together."),
            _("I'm tired all the time. I sat down for five minutes yesterday and woke up two hours later."),
            _("I cried at a commercial this morning. A commercial. About a bank."),
        ],
    }

    _PREG_CHITCHAT_LATE = {
        "gwen": [
            _("Oh! The baby kicked! Come here, feel this!"),
            _("This kid kicks harder than I ever kicked in gym class. Takes after me, I guess."),
            _("My back is KILLING me. I can't sit, I can't stand, I can't lie down. Nothing works."),
            _("I haven't seen my own feet in weeks. They could be purple for all I know."),
            _("I've been looking at baby names. Nothing feels right. This is harder than naming a band."),
            _("I bought a tiny onesie today. The smallest piece of clothing I've ever seen. And I cried in the store. Me. Crying over a onesie."),
        ],
        "rogue": [
            _("The baby was moving all night. I couldn't sleep at all."),
            _("Sometimes I just sit there with my hand on my belly, waiting for the next one. It never gets old."),
            _("My ankles are so swollen I can't wear my boots anymore. That's where I draw the line."),
            _("Getting up from a chair has become a whole production. I need a countdown and a launch sequence."),
            _("My aunt called. She's already knitting baby blankets. Hasn't even met the baby yet and it's already spoiled."),
            _("I've been thinking about what kind of mom I want to be. I want to be the kind who's always there."),
        ],
        "ntw": [
            _("This thing kicked me in the ribs. MY OWN CHILD assaulted me from the inside."),
            _("It keeps moving when I try to sleep. Midnight is NOT playtime. We need to have a talk."),
            _("My center of gravity is completely off. I almost fell down the stairs twice today."),
            _("I waddle now. I WADDLE. If anyone laughs, I'm throwing hands."),
            _("I refuse to be one of those moms who posts baby pictures every five minutes. The kid deserves some privacy."),
            _("I looked at daycare prices. I think I blacked out for a second."),
        ],
        "tenny": [
            _("The baby kicked during my exam! I almost screamed in the middle of the lecture hall!"),
            _("I talk to the baby sometimes when I'm studying. I read somewhere they can hear you..."),
            _("I-I can't reach the top shelf in the lab anymore... my belly gets in the way..."),
            _("Sleeping is so hard now... I need like five pillows and I still can't get comfortable."),
            _("My grandpa sent a huge care package... baby clothes, books, even a tiny lab coat. He's so excited."),
            _("I've been planning my schedule around the due date. If I take summer classes, I can still graduate on time..."),
        ],
        "_default": [
            _("The baby kicked again. Here, give me your hand. Feel that?"),
            _("My back hurts, my feet hurt, and I can't see my own shoes anymore."),
            _("Sleeping is a whole project now. Pillows everywhere, and I still wake up every hour."),
            _("I've started looking at baby names. Everything sounds wrong and I change my mind every day."),
            _("I bought the first tiny outfit yesterday. I just stood there in the store holding it for ten minutes."),
            _("People keep giving me their seat now. I hate how much I need it."),
        ],
    }

    # NPC "parent" chitchat. "male" = lines only a man can say (dad / father / the only guy).
    # "fooled" = lines only a partner who BELIEVES the child is his can say (child_father_fooled, children.rpy):
    # _npc_paternity_claimed is also true for the NTR boundary level 4 partner, who KNOWS and said "I'll raise
    # the kid", and that is the only way a female partner gets here (never Choice 4).
    # The baby lives with HER family: he visits, he does not lose sleep over a baby in the next room.
    _PREG_NPC_CHITCHAT_EARLY = {
        "any": [
            _("I've been looking at cribs online. They're so expensive, dude. Being a parent is no joke."),
            _("She's been having these crazy cravings. I went to three stores last night to find pickles and chocolate syrup."),
            _("I started reading parenting books. Did you know babies can't see colors for the first few months? Wild."),
            _("She threw up this morning and I just held her hair. That's love, right? Holding someone's hair while they puke."),
        ],
        "male": [
            _("I'm scared, honestly. Like, what if I'm a terrible father? What do I even know about babies?"),
        ],
        "fooled": [
            _("Hey man, %s told me the news. I'm gonna be a dad! Can you believe it?"),
        ],
    }

    _PREG_NPC_CHITCHAT_LATE = {
        "any": [
            _("We felt the baby kick last night. Like, actually KICK. It's real now, you know? Really real."),
            _("I've been building a crib. Well, trying to. The instructions are in Swedish and I'm missing two screws."),
            _("I can't stop buying tiny socks. They're so SMALL. Have you ever seen socks this small?"),
            _("Her belly is getting so big. She's beautiful though. Don't tell her I said that, she'll punch me."),
        ],
        "male": [
            _("I signed up for a parenting class. Just me and a room full of couples. I was the only guy there alone because she had class."),
        ],
    }

    def _preg_npc_present(girl):
        """Her NPC partner is ON SCREEN with her right now (store._npc_on_scene, set by
        resolve_npc_for_location). Only then can HE say a line in the middle of her chitchat: never over
        the phone, never while he is somewhere else."""
        if getattr(store, "_phone_mode", False):
            return False
        _npc = get_npc_partner_for(girl)
        return _npc is not None and _npc is getattr(store, "_npc_on_scene", None)

    def _preg_npc_chitchat_say(girl, pools):
        """Her NPC partner talks about the baby. pools = {"any": [...], "male": [...]} (see above)."""
        npc = get_npc_partner_for(girl)
        if not npc:
            return
        _g = getattr(npc, "gender", "male")
        _pool = pools.get("any", []) + pools.get(_g, [])
        if child_father_fooled(girl):
            _pool = _pool + pools.get("fooled", [])
        if not _pool:
            return
        _line = _tl(renpy.random.choice(_pool))
        if "%s" in _line:
            # only one line carries her name: "% girl.Name" on the others raised TypeError (5 lines out of 6)
            _line = _line % girl.Name
        print("[PREGNANCY] npc chitchat: %s gender=%s pool=%d" % (npc.Name, _g, len(_pool)))
        Character(npc.Name)(_line)

    def chitchat_pregnancy_early(girl, loc, t_index):
        pool = girl_pool(_PREG_CHITCHAT_EARLY, girl, "chitchat early")
        set_scene_expression(girl, "worried")
        Say_Line(girl, _tl(renpy.random.choice(pool)))
        set_scene_expression(girl, "normal")

    def chitchat_pregnancy_late(girl, loc, t_index):
        pool = girl_pool(_PREG_CHITCHAT_LATE, girl, "chitchat late")
        expr = renpy.random.choice(["worried", "smile", "sad"])
        set_scene_expression(girl, expr)
        Say_Line(girl, _tl(renpy.random.choice(pool)))
        set_scene_expression(girl, "normal")

    def chitchat_npc_pregnancy_early(girl, loc, t_index):
        _preg_npc_chitchat_say(girl, _PREG_NPC_CHITCHAT_EARLY)

    def chitchat_npc_pregnancy_late(girl, loc, t_index):
        _preg_npc_chitchat_say(girl, _PREG_NPC_CHITCHAT_LATE)

    # Registration: pregnancy early (stage 2)
    register_chitchat(
        "global",
        chitchat_pregnancy_early,
        condition=lambda g, loc, t: (
            getattr(g, "_pregnant", False)
            and getattr(g, "_pregnancy_stage", 0) == 2
            and getattr(g, "_pregnancy_known", False)
        ),
        weight=4,
    )

    # Registration: pregnancy late (stage 3)
    register_chitchat(
        "global",
        chitchat_pregnancy_late,
        condition=lambda g, loc, t: (
            getattr(g, "_pregnant", False)
            and getattr(g, "_pregnancy_stage", 0) >= 3
            and getattr(g, "_pregnancy_known", False)
        ),
        weight=4,
    )

    # Registration: NPC "father" chitchat early (stage 2, paternity claimed)
    register_chitchat(
        "global",
        chitchat_npc_pregnancy_early,
        condition=lambda g, loc, t: (
            getattr(g, "_pregnant", False)
            and getattr(g, "_pregnancy_stage", 0) == 2
            and getattr(g, "_npc_paternity_claimed", False)
            and _preg_npc_present(g)
        ),
        weight=3,
    )

    # Registration: NPC "father" chitchat late (stage 3, paternity claimed)
    register_chitchat(
        "global",
        chitchat_npc_pregnancy_late,
        condition=lambda g, loc, t: (
            getattr(g, "_pregnant", False)
            and getattr(g, "_pregnancy_stage", 0) >= 3
            and getattr(g, "_npc_paternity_claimed", False)
            and _preg_npc_present(g)
        ),
        weight=3,
    )

    # ── Postpartum chitchat pools (Phase 7) ──
    # A plain line is true at ANY age. A line that dates the baby carries its age tiers:
    #   (line, first_tier, last_tier)   tiers = newborn / infant / baby / toddler (children.rpy _CHILD_AGE_TIERS)
    # They used to play from the day she came back: "the baby is three months old", "smiled for the first time".
    # Every pool must keep plain lines (the picker falls back to them); "_default" is all plain on purpose.

    _PREG_CHITCHAT_POSTPARTUM = {
        "gwen": [
            _("My mom sent me a picture of the baby in this tiny leather jacket. I didn't ask for it but... okay, it's adorable."),
            _("Apparently my kid already has a personality. My mom says they scream at everything. Takes after me."),
            (_("I video called home yesterday. The baby grabbed the phone and drooled on it. That's basically a kiss, right?"), "baby", "toddler"),
            _("My mom keeps asking when I'm coming to visit. I told her after finals. She said the baby won't remember me. Thanks, mom."),
            (_("I bought the tiniest pair of boots online. I know the baby can't walk yet. I don't care."), "newborn", "baby"),
            _("My parents are spoiling that kid rotten. I already see it. By the time I graduate they'll have more toys than a store."),
            (_("The baby laughs at everything now. Even at my jokes. Finally, an audience with taste."), "baby", "baby"),
            (_("My mom says the baby rolled over and looked very smug about it. Wonder where that comes from."), "baby", "baby"),
            (_("First steps happened. I watched the video about thirty times. I'm not crying, shut up."), "toddler", "toddler"),
            (_("The kid has started saying 'no' to everything. I've never been more proud."), "toddler", "toddler"),
        ],
        "rogue": [
            _("My aunt called. Baby's checkup went great. Growing like a weed, she says."),
            _("I asked my aunt to send me updates every day. She sends about twelve. I'm not complaining."),
            (_("The baby smiled for the first time yesterday. My aunt sent me a video and I watched it forty times."), "infant", "infant"),
            _("I worry sometimes. Being this far away from my baby... is that selfish? My aunt says it's not, but she has to say that."),
            _("My aunt made this whole schedule. Doctor visits, vaccinations, feeding times. That woman runs a tighter ship than the military."),
            _("Sometimes I hear a baby crying on campus and my heart stops for a second. Every single time."),
            (_("Baby's sittin' up all alone now. My aunt says I did it at the same age."), "baby", "baby"),
            (_("That little one grabs everything in reach. My aunt's hidin' the good dishes."), "baby", "baby"),
            (_("Baby took the first steps across my aunt's kitchen. I cried right there on the phone."), "toddler", "toddler"),
            (_("The little one climbs everythin' now. My aunt says she needs eyes in the back of her head."), "toddler", "toddler"),
        ],
        "ntw": [
            _("My mom sent a picture. The kid's making this angry face. I've never been more proud."),
            _("Apparently the baby won't stop screaming at 3 AM. Join the club, kid."),
            _("I'm NOT one of those moms who shows baby pictures to everyone. But do you want to see one? Just one. Whatever."),
            _("My mom says the baby has my eyes. My mom also says I should call more. I'm ignoring both of those."),
            (_("The kid bit my mom. ALREADY. They don't even have real teeth yet. That's raw talent."), "infant", "baby"),
            _("I don't miss the baby. I DON'T. I'm just... checking in a lot. For logistical purposes."),
            (_("The kid can sit up now. Glares at everyone from a higher angle."), "baby", "baby"),
            (_("The baby threw a rattle across the room. Good arm."), "baby", "baby"),
            (_("The kid walks now. Runs, actually. Straight at things that break."), "toddler", "toddler"),
            (_("First word was 'no'. Obviously."), "toddler", "toddler"),
        ],
        "tenny": [
            (_("My grandpa reads to the baby every night. Science books. The baby is three months old. Grandpa doesn't care, he says it's never too early."), "infant", "infant"),
            _("I started a savings account for the baby's college fund. It only has forty dollars in it but it's a start!"),
            _("I cried in the library yesterday because I saw a baby blanket in a store window. I'm fine. Totally fine."),
            (_("Grandpa sent me a drawing the baby 'made.' It's a scribble. I hung it on my wall. It's the best art I've ever seen."), "baby", "toddler"),
            _("I calculated how much college will cost in eighteen years. Then I closed the spreadsheet and took a nap."),
            (_("The baby said something that sounded like a word yesterday. Grandpa swears it was 'data.' I think it was a burp, but I'm choosing to believe him."), "baby", "baby"),
            (_("G-grandpa says the baby stares at his toolbox for hours. He's so proud."), "baby", "baby"),
            (_("The baby learned to clap! Grandpa claps back. They do it for ten minutes straight."), "baby", "baby"),
            (_("The baby is walking! Grandpa baby-proofed my parents' whole house in one night. He brought his own tools."), "toddler", "toddler"),
            (_("Grandpa is teaching the baby to count. They're at three. H-he says that's advanced."), "toddler", "toddler"),
        ],
        # all plain (true at any age) on purpose: this is the fallback of every pool
        "_default": [
            _("My family sends me pictures of the baby every day. I've looked at each one about a hundred times."),
            _("I called home last night just to hear the baby in the background. It made my whole day."),
            _("It's strange being back here while the baby is at home. Part of me is always somewhere else now."),
            _("My family says the baby is doing great. Eating well, sleeping... sometimes."),
            _("I keep buying little things for the baby. My bag for the next trip home is already full."),
            _("I never thought I'd be the kind of person who shows baby pictures. Do you want to see one?"),
        ],
    }

    _PREG_CHITCHAT_POSTPARTUM_MULTI = {
        "gwen": [
            _("Having two is a whole different beast. My mom says she's aged ten years in a month."),
            _("The kids fight over the dumbest stuff already. I can relate, honestly."),
            _("My parents keep sending me videos of the kids together. My storage is screaming."),
        ],
        "rogue": [
            _("Two babies, sugar. My aunt says the house sounds like a zoo and she wouldn't change a thing."),
            _("The kids are drivin' my aunt crazy, but the good kind of crazy."),
        ],
        "ntw": [
            _("Two kids. I have TWO kids. How did that happen? Don't answer that."),
            _("My mom says the older one bosses the younger one around. Runs in the family."),
        ],
        "tenny": [
            _("G-grandpa says having two is easier because they entertain each other. I think he's lying."),
            _("The kids keep grandpa on his toes. He says it keeps him young!"),
        ],
        "_default": [
            _("Having more than one kid is... a lot. But in a good way, I think."),
            _("My family is busy with the kids. They never run out of stories to tell me."),
            _("The kids are growing so fast. Every call home sounds different."),
        ],
    }

    _PREG_NPC_CHITCHAT_POSTPARTUM = {
        "any": [
            _("When we go see the baby, I get my finger grabbed and I don't get it back. I almost cry every time."),
            _("Every trip to see the baby wrecks me. Then the baby looks at me and I forget I'm exhausted."),
            _("Her family is helping out a lot. I don't know what we'd do without them honestly."),   # "family": a shared line must fit every girl's family story
            _("I keep buying stuff for the baby. I walked past a toy store and just... couldn't help myself."),
        ],
        "male": [
            _("Man, being a dad is... I don't even have words. The best and scariest thing at the same time."),
        ],
        "fooled": [
            _("Everyone says the baby looks like me. I mean... yeah, of course it does."),
        ],
    }

    def chitchat_postpartum(girl, loc, t_index):
        # baby_line_pick (children.rpy): her pool, true for the baby's age, never a line he already heard
        expr = renpy.random.choice(["smile", "worried", "normal"])
        set_scene_expression(girl, expr)
        Say_Line(girl, _tl(baby_line_pick(girl)))
        set_scene_expression(girl, "normal")

    def chitchat_npc_postpartum(girl, loc, t_index):
        _preg_npc_chitchat_say(girl, _PREG_NPC_CHITCHAT_POSTPARTUM)

    # Registration: postpartum girl chitchat (permanent after birth)
    register_chitchat(
        "global",
        chitchat_postpartum,
        # a "distant" mother (he denied the child and has not made up for it) does not volunteer baby talk:
        # her mood sets the tone of EVERY line about the baby (children.rpy mother_mood)
        condition=lambda g, loc, t: getattr(g, "_postpartum", False) and mother_mood(g) != "distant",
        weight=2,
    )
    # A topic plays once per cycle of ALL her topics (weight is not frequency): an older baby, with more to
    # tell, gets a second slot in the cycle. Same function, same picker, no repeated line (baby_line_pick).
    register_chitchat(
        "global",
        chitchat_postpartum,
        condition=lambda g, loc, t: (getattr(g, "_postpartum", False) and mother_mood(g) != "distant"
                                     and child_age_tier(g) in ("baby", "toddler")),
        weight=2,
    )

    # Registration: NPC "father" postpartum (permanent, paternity claimed)
    register_chitchat(
        "global",
        chitchat_npc_postpartum,
        condition=lambda g, loc, t: (
            getattr(g, "_postpartum", False)
            and getattr(g, "_npc_paternity_claimed", False)
            and _preg_npc_present(g)
        ),
        weight=2,
    )

    # ==========================================================
    # PREGNANCY CHITCHAT: her mood about the future, "do you want kids?", the OTHER girls noticing
    # ==========================================================

    # --- Pregnant and he knows: worry / hope about what comes next (dialogue_bank pools) ---
    # A pregnancy trait settles her mood. Otherwise how he answered at the discovery event and how much
    # she loves him do, and both pools can be open at once.
    _PREG_CASUAL_EXPR = {"pregnancy_casual_worry": "worried", "pregnancy_casual_positive": "smile"}
    _PREG_CASUAL_TRAIT_MOOD = {"pregnancy_fear": "pregnancy_casual_worry", "pregnancy_fetish": "pregnancy_casual_positive"}
    _PREG_CASUAL_WORRY_RESPONSES = ("deny", "npc_paternity")
    _PREG_CASUAL_POSITIVE_RESPONSES = ("supportive", "breeding")
    _PREG_CASUAL_LOVE_SPLIT = 500

    def _preg_casual_moods(girl):
        """dialogue_bank keys she can speak from right now ([] = not pregnant, or he does not know yet)."""
        if not (getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False)):
            return []
        for _trait, _key in _PREG_CASUAL_TRAIT_MOOD.items():
            if girl.has_trait(_trait):
                return [_key]
        _resp = getattr(girl, "_player_pregnancy_response", None)
        _moods = []
        if _resp in _PREG_CASUAL_WORRY_RESPONSES or girl.Love < _PREG_CASUAL_LOVE_SPLIT:
            _moods.append("pregnancy_casual_worry")
        if _resp in _PREG_CASUAL_POSITIVE_RESPONSES or girl.Love >= _PREG_CASUAL_LOVE_SPLIT:
            _moods.append("pregnancy_casual_positive")
        return _moods

    def _chitchat_pregnancy_casual(girl, key):
        set_scene_expression(girl, _PREG_CASUAL_EXPR[key])
        Say_Line(girl, rod_pick_line(girl, key))
        set_scene_expression(girl, "normal")
        print("[PREGNANCY] chitchat %s: %s (response=%s Love=%d)" % (key, girl.gid, getattr(girl, "_player_pregnancy_response", None), girl.Love))

    def chitchat_pregnancy_worry(girl, loc, t_index):
        _chitchat_pregnancy_casual(girl, "pregnancy_casual_worry")

    def chitchat_pregnancy_positive(girl, loc, t_index):
        _chitchat_pregnancy_casual(girl, "pregnancy_casual_positive")

    register_chitchat("global", chitchat_pregnancy_worry,
        condition=lambda g, loc, t: "pregnancy_casual_worry" in _preg_casual_moods(g), weight=3)
    register_chitchat("global", chitchat_pregnancy_positive,
        condition=lambda g, loc, t: "pregnancy_casual_positive" in _preg_casual_moods(g), weight=3)

    # --- Not pregnant: he asks whether she ever thinks about kids (dialogue_bank "pregnancy_ask_about_kids*") ---
    _PREG_KIDS_MIN_LOVE = 300
    _PREG_KIDS_QUESTIONS = [
        _("Random question. Do you ever think about having kids someday?"),
        _("Can I ask you something? Do you see yourself as a mom one day?"),
    ]
    # A pregnancy trait overrides the Love tier, and saying that line is what reveals the trait.
    _PREG_KIDS_TRAIT_TIER = {"pregnancy_fear": "fear", "pregnancy_fetish": "fetish"}
    _PREG_KIDS_KEY = {
        "low": "pregnancy_ask_about_kids", "mid": "pregnancy_ask_about_kids_mid", "high": "pregnancy_ask_about_kids_high",
        "fetish": "pregnancy_ask_about_kids_fetish", "fear": "pregnancy_ask_about_kids_fear",
    }
    _PREG_KIDS_EXPR = {"low": "thinking", "mid": "shy", "high": "embarrassed", "fetish": "embarrassed", "fear": "nervous"}
    _PREG_KIDS_EFFECTS = {"high": (("Love", 3),), "fetish": (("Love", 3), ("Lust", 5)), "fear": (("Love", -3),)}

    def _preg_kids_tier(girl):
        for _trait, _tier in _PREG_KIDS_TRAIT_TIER.items():
            if girl.has_trait(_trait):
                return _tier
        if girl.Love >= 800 and girl.is_dating_player():
            return "high"
        return "mid" if girl.Love >= 500 else "low"

    def _preg_kids_available(girl):
        if store._pregnancy_mode == "off" or girl.Love < _PREG_KIDS_MIN_LOVE:
            return False
        if getattr(girl, "_postpartum", False) or getattr(girl, "_giving_birth", False):
            return False
        # once he knows she is pregnant the question is moot (her casual pools take over)
        return not (getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False))

    def chitchat_ask_about_kids(girl, loc, t_index):
        _tier = _preg_kids_tier(girl)
        Say_Player(renpy.random.choice(_PREG_KIDS_QUESTIONS))
        set_scene_expression(girl, _PREG_KIDS_EXPR[_tier])
        Say_Line(girl, rod_pick_line(girl, _PREG_KIDS_KEY[_tier]))
        for _stat, _amount in _PREG_KIDS_EFFECTS.get(_tier, ()):
            Change_Status(girl, _stat, _amount)
        for _trait, _t in _PREG_KIDS_TRAIT_TIER.items():
            if _t == _tier:
                girl.discover("discovered_trait_" + _trait)
        set_scene_expression(girl, "normal")
        print("[PREGNANCY] chitchat ask_about_kids: %s tier=%s Love=%d dating=%s" % (girl.gid, _tier, girl.Love, girl.is_dating_player()))

    register_chitchat("global", chitchat_ask_about_kids,
        condition=lambda g, loc, t: _preg_kids_available(g), weight=2)

    # --- ANOTHER girl is showing / in labor / a mother: the speaker comments on it ---
    # Angle, by what the speaker can see and knows (_preg_other_girl_angle):
    #   "suspect"        that girl is at stage 2 (small bump, loose clothes, morning sickness)
    #   "know_player"    stage 3 and the speaker knows he sleeps with that girl, or that girl dates him
    #   "know_partner"   stage 3 and that girl has a boyfriend / girlfriend: the natural guess
    #   "know"           stage 3, nobody obvious
    #   "in_labor"       that girl left campus to give birth (the week away is no longer silent)
    #   "mom" / "mom_partner" / "mom_player"   the same three, once the baby is born
    #   "co_mother"      the speaker ALSO has a child of his and knows this one is his too (belly or baby):
    #                    THE beat of several mothers. Lines must work for a belly and for a born baby.
    #   "my_girl" / "my_girl_player"   that girl is the SPEAKER'S girlfriend (the person with the most at
    #                    stake used to be the only one who never said a word); "_player" = she knows it is his.
    #                    Lines must work for a belly and for a born baby.
    # The fallback is PER ANGLE (girl_pool with key): a pool writes only the angles it wants.
    # %(name)s = the pregnant girl, %(pl)s = her partner label ("boyfriend" / "girlfriend"). The POOL is
    # the speaker's; a girl with no pool here uses "_default". No line may assume the partner's gender.
    _PREG_OTHER_GIRL_LINES = {
        "gwen": {
            "suspect": [
                _("Have you seen %(name)s lately? Baggy hoodies, skipping coffee, that little glow. I have a theory."),
                _("%(name)s ran out of class looking green this morning. Either the cafeteria struck again or something's up."),
                _("Call it goth intuition, but %(name)s is hiding something under all those loose shirts."),
            ],
            "know": [
                _("So %(name)s is pregnant. Like, visibly. There is no hoodie on Earth big enough anymore."),
                _("Did you see %(name)s today? That is not a food baby. I wonder who the dad is."),
                _("%(name)s waddled past me in the hall. I almost offered to carry her books. Almost."),
            ],
            "know_partner": [
                _("%(name)s and her %(pl)s are having a baby, huh? Wild. They don't strike me as the crib-shopping type."),
                _("I saw %(name)s with that belly. Her %(pl)s must be freaking out. In a good way. Probably."),
                _("Somebody should warn %(name)s's %(pl)s that babies don't come with an off switch."),
            ],
            "know_player": [
                _("So. %(name)s is pregnant. And I happen to know who's been keeping her company. Anything you want to tell me?"),
                _("Funny thing about %(name)s's belly. I can count, you know. And I know where you've been."),
                _("%(name)s is showing, and you've gone very quiet about it. The 'I did that' kind of quiet. Don't even try to deny it."),
            ],
            "in_labor": [
                _("%(name)s is off having an actual baby right now. And I thought my week was intense."),
            ],
            "mom": [
                _("%(name)s came back a mom. Same girl, new eye bags. Motherhood looks brutal."),
            ],
            "mom_partner": [
                _("%(name)s's %(pl)s is pushing baby photos on everyone. Somebody take that phone away."),
            ],
            "mom_player": [
                _("%(name)s had your kid. Congrats, I guess? You seem way too calm for someone with a baby."),
            ],
            "co_mother": [
                _("So %(name)s and I are both in your little club now. Should we get jackets?"),
            ],
            "my_girl": [
                _("My girlfriend and a baby I had nothing to do with. Obviously. I'm handling it great, can't you tell?"),
            ],
            "my_girl_player": [
                _("You got MY girlfriend pregnant. Do you just collect disasters, or is it a talent?"),
            ],
        },
        "rogue": {
            "suspect": [
                _("Sugar, have you noticed %(name)s lately? Loose tops, turning down coffee. I've got a feeling."),
                _("%(name)s about lost her breakfast in the hall today. Poor thing. I wonder if it's what I think it is."),
                _("Something's different about %(name)s. She's got that glow my aunt always talked about."),
            ],
            "know": [
                _("Well, there's no hiding it now. %(name)s is expecting. That belly says it all."),
                _("Did you see %(name)s? Bless her heart, she's carrying that baby like a champ. I wonder who the daddy is."),
                _("%(name)s let me feel the baby kick today. I ain't gonna lie, I teared up a little."),
            ],
            "know_partner": [
                _("%(name)s and her %(pl)s are having a baby. I hope they know what they're in for."),
                _("I saw %(name)s's %(pl)s carrying her bag for her today. That's sweet. That's how it should be."),
                _("A baby on the way for %(name)s and her %(pl)s. Lord, time moves fast around here."),
            ],
            "know_player": [
                _("So %(name)s is pregnant. And I know you two have been close, sugar. Real close. Is it yours?"),
                _("I saw %(name)s's belly today, and I did some thinking about who's been around her. You got something to say?"),
                _("%(name)s is carrying a baby, and I've got a pretty good idea whose. I hope you're doing right by her."),
            ],
            "in_labor": [
                _("%(name)s went home to have her baby, sugar. I lit a little candle for her. Don't laugh."),
            ],
            "mom": [
                _("%(name)s is a mama now. She showed me a picture and I near about melted."),
            ],
            "mom_partner": [
                _("%(name)s's %(pl)s won't stop talkin' about that baby. It's the sweetest thing."),
            ],
            "mom_player": [
                _("%(name)s had your baby, sugar. You asked her about that baby yet? You better have."),
            ],
            "co_mother": [
                _("Me and %(name)s got more in common than I figured. Both of us, and you. Lord have mercy."),
            ],
            "my_girl": [
                _("%(name)s is my girl, sugar. And that baby ain't mine, no way around it. I'm tryin' real hard to be okay."),
            ],
            "my_girl_player": [
                _("You and %(name)s. My girl. I oughta slap you into next week, and I still might."),
            ],
        },
        "ntw": {
            "suspect": [
                _("%(name)s has been wearing hoodies in this heat and skipping gym. Something's off."),
                _("%(name)s threw up behind the bleachers. Twice. I'm not a doctor, but I can do math."),
                _("Is it just me, or is %(name)s hiding something? She flinched when I mentioned her jeans."),
            ],
            "know": [
                _("%(name)s is pregnant. Very pregnant. You can see it from across the quad."),
                _("So %(name)s has a whole human in there now. Who's the dad? Not that I care."),
                _("%(name)s asked me to carry her bag. I did it. If you tell anyone, you die."),
            ],
            "know_partner": [
                _("%(name)s and her %(pl)s are having a kid. Better them than me."),
                _("I saw %(name)s's %(pl)s reading a baby book in the library. Absolutely terrified. Good."),
                _("%(name)s is showing. Her %(pl)s keeps grinning like an idiot. It's unbearable."),
            ],
            "know_player": [
                _("%(name)s is pregnant. And I know you've been sleeping with her. Do the math for me."),
                _("Saw %(name)s's belly. Saw your face when she walked by. You're not subtle."),
                _("So you knocked up %(name)s. Wow. Congratulations on making everything more complicated."),
            ],
            "in_labor": [
                _("%(name)s left to give birth. Campus is quieter. Don't tell her I noticed."),
            ],
            "mom": [
                _("%(name)s is back. With baby pictures. She showed me twelve. I counted."),
            ],
            "mom_partner": [
                _("%(name)s's %(pl)s keeps grinning at strangers. Babies break people."),
            ],
            "mom_player": [
                _("%(name)s had your kid. So that's a thing you do now."),
            ],
            "co_mother": [
                _("%(name)s too? Great. You're building a team."),
            ],
            "my_girl": [
                _("My girlfriend, and a baby that is not mine. Ask me how I feel. Actually, don't."),
            ],
            "my_girl_player": [
                _("You. %(name)s. A baby. Give me one reason not to break your nose."),
            ],
        },
        "tenny": {
            "suspect": [
                _("H-have you noticed %(name)s lately? She's been wearing really loose clothes, and she looks so tired..."),
                _("%(name)s got sick in the lab today. She said it was nothing, but the symptoms match something I read..."),
                _("I don't want to gossip, but... I think %(name)s might be hiding something. Statistically, it fits."),
            ],
            "know": [
                _("%(name)s is pregnant! I-I mean, it's obvious now. I hope she's doing okay..."),
                _("I saw %(name)s today and her belly is so big already. I wonder who the father is..."),
                _("I offered %(name)s my seat in the lecture hall. She looked so relieved. Carrying a baby must be exhausting."),
            ],
            "know_partner": [
                _("%(name)s and her %(pl)s are going to be parents! That's... wow. That's so grown up."),
                _("I saw %(name)s's %(pl)s buying baby clothes downtown. It was kind of adorable."),
                _("%(name)s and her %(pl)s must be so nervous. I would be. I'd make so many lists."),
            ],
            "know_player": [
                _("U-um... %(name)s is pregnant. And I know you two have been... together. Is it... yours?"),
                _("I saw %(name)s's belly. And I know about you and her. I-I'm not judging! I just... noticed."),
                _("%(name)s is having a baby, and I think I know whose it is... you should be nice to her, okay?"),
            ],
            "in_labor": [
                _("%(name)s went home for the b-birth! I hope she's okay. I read that it can take hours."),
            ],
            "mom": [
                _("%(name)s showed me the baby pictures! S-so tiny. I almost cried in the hallway."),
            ],
            "mom_partner": [
                _("%(name)s's %(pl)s carries baby pictures everywhere now. I-it's really sweet."),
            ],
            "mom_player": [
                _("%(name)s had your baby... A-are you helping her? You should be helping her."),
            ],
            "co_mother": [
                _("%(name)s and I talked about babies for an hour. I-it's strange. But kind of nice?"),
            ],
            "my_girl": [
                _("%(name)s is my g-girlfriend. And the baby isn't... I mean, it can't be mine. I don't know what to do."),
            ],
            "my_girl_player": [
                _("Y-you and %(name)s... She's MY girlfriend! How could you do that to me?"),
            ],
        },
        "_default": {
            "suspect": [
                _("Have you noticed %(name)s lately? Loose clothes, always tired. I think something's going on."),
                _("%(name)s got sick in the hallway this morning. I have a guess about why."),
            ],
            "know": [
                _("%(name)s is pregnant. You can't miss it anymore."),
                _("Did you see %(name)s? That belly is getting big. I wonder who the father is."),
            ],
            "know_partner": [
                _("%(name)s and her %(pl)s are having a baby. Big changes for them."),
                _("I saw %(name)s's %(pl)s fussing over her today. It was kind of sweet."),
            ],
            "know_player": [
                _("%(name)s is pregnant. And I know you two have been close. Is there something I should know?"),
                _("I saw %(name)s's belly. I think we both know who's responsible."),
            ],
            "in_labor": [
                _("%(name)s left campus this week. The baby is coming. Can you believe it?"),
                _("Did you hear? %(name)s went home to have the baby. I hope everything goes well."),
            ],
            "mom": [
                _("%(name)s is back, and she's a mom now. It still sounds strange to say."),
                _("I saw %(name)s showing baby pictures in the hall. She looks exhausted and happy."),
            ],
            "mom_partner": [
                _("%(name)s and her %(pl)s have a baby now. Every free weekend they are on the road to see the little one."),
                _("I ran into %(name)s's %(pl)s. The baby is all they talk about."),
            ],
            "mom_player": [
                _("So %(name)s had the baby. Your baby. Are you ever going to talk about it?"),
                _("%(name)s is a mom now. And you're a dad. Does that feel real to you yet?"),
            ],
            "co_mother": [
                _("%(name)s and I have something in common now. You."),
                _("So %(name)s too. Your kids are going to have a lot of siblings to keep track of."),
            ],
            "my_girl": [
                _("%(name)s and I are supposed to be a couple. And now there's a baby that sure isn't mine. I don't know how to feel."),
                _("I love %(name)s. But every time I think about that baby, I wonder who else she loves."),
            ],
            "my_girl_player": [
                _("You and %(name)s. My girlfriend. A baby. Do you have any idea what that did to us?"),
                _("I know the baby is yours. Don't insult me by denying it."),
            ],
        },
    }
    # "Another baby" variants: mixed into the pool when the girl being talked about already has children
    # and is pregnant again. Only for "currently pregnant" angles; birth/mom angles are about THIS child.
    _PREG_OTHER_GIRL_LINES_AGAIN = {
        "_default": {
            "suspect": [
                _("Is %(name)s pregnant AGAIN? The loose clothes, the tiredness... I've seen this before."),
                _("Didn't %(name)s just have a baby? And now she's looking like that again?"),
            ],
            "know": [
                _("%(name)s is pregnant again. She already has a kid, and now another one on the way."),
                _("Another baby for %(name)s. She's really going for it, huh."),
            ],
            "know_partner": [
                _("%(name)s and her %(pl)s are having another baby. They must love the chaos."),
                _("Another one for %(name)s and her %(pl)s. They're building a whole family."),
            ],
            "know_player": [
                _("%(name)s is pregnant again. And I bet I know who's responsible. Again."),
                _("Another baby, and I already know whose it is. You really can't help yourself."),
            ],
        },
    }

    # expression per angle; "jealous" = the speaker dates him, is not polyamorous, and never accepted that girl
    _PREG_OTHER_GIRL_EXPR = {"suspect": "thinking", "know": "surprised", "know_partner": "smile", "know_player": "smirk", "jealous": "annoyed",
                             "in_labor": "surprised", "mom": "smile", "mom_partner": "smile", "mom_player": "smirk",
                             "co_mother": "thinking", "my_girl": "sad", "my_girl_player": "angry"}
    _PREG_OTHER_GIRL_JEALOUSY = 15      # once per pair and per phase (belly / born baby), the first time she says it to his face
    # angles where the speaker tells him to his face that the child is HIS: a girlfriend who never accepted that girl is jealous
    _PREG_OTHER_GIRL_HIS_ANGLES = ("know_player", "mom_player", "co_mother", "my_girl_player")
    _PREG_OTHER_GIRL_MOM_DAYS = 60      # a born baby is campus talk for this many days (co-mothers never run out)
    _MOM_NEWS_DAYS = 10                 # fresh news (top of Chit_Chat): this long after she is back
    _MOM_NEWS_CHANCE = 0.5

    def _preg_other_girl_state(other):
        """What the campus can SEE about that girl: "in_labor" / "showing" / "mom", or None. A mother who is
        pregnant again is "showing": the new belly is the news (chitchat_pregnant_friend mixes the AGAIN lines in)."""
        if getattr(other, "_giving_birth", False):
            return "in_labor"
        if getattr(other, "_pregnant", False) and getattr(other, "_pregnancy_stage", 0) >= 2:
            return "showing"
        if girl_is_mother(other):
            return "mom"
        return None

    def _preg_other_girl_targets(girl):
        """Girls the speaker can comment on: showing (stage 2+), in labor, or a mother whose baby is still
        news (for a co-mother it never stops being a subject). Never herself."""
        _out = []
        # campus talk: a girl who lives off campus neither gossips about the campus girls nor is their gossip
        if girl_off_campus(girl):
            return _out
        for _o in ALL_GIRLS:
            _state = _preg_other_girl_state(_o)
            if _o.gid == girl.gid or _state is None or girl_off_campus(_o):
                continue
            if (_state == "mom" and (child_age_days(_o) or 0) > _PREG_OTHER_GIRL_MOM_DAYS
                    and _preg_other_girl_angle(girl, _o) != "co_mother"):
                continue
            _out.append(_o)
        return _out

    def _preg_other_girl_angle(girl, other):
        _state = _preg_other_girl_state(other)
        _his = other.is_dating_player() or girl_knows_with_player(girl, other, "sex")
        # DORMANT today: nothing in the game writes girl_partner_id yet (Girl.set_girl_partner has no caller).
        # The day playable girls can date each other these two angles wake up by themselves. Not for a speaker
        # who dates HIM and accepted that girl in her harem: "how could you do that to me" would be wrong.
        if (getattr(girl, "girl_partner_id", None) == other.gid
                and not (girl.is_dating_player() and other.gid in (getattr(girl, "harem_accepted", None) or set()))):
            return "my_girl_player" if _his else "my_girl"
        if _state == "in_labor":
            return "in_labor"
        _mom = (_state == "mom")
        if not _mom and getattr(other, "_pregnancy_stage", 0) < 3:
            return "suspect"
        if _his:
            # never in front of the speaker's OWN fooled partner: "both of us, and you" gives her secret away
            # (children.rpy mother_hush, the rule her "How's the baby?" answer already follows)
            if girl_is_mother(girl) and not mother_hush(girl):
                return "co_mother"
            return "mom_player" if _mom else "know_player"
        # a partner who already confronted the player KNOWS it is not his: the "her boyfriend keeps grinning
        # like an idiot" guess would contradict what half the campus watched. Once the baby is BORN the guess
        # is only true for the partner who stands as the father: a boyfriend she found after the birth (or an
        # ex who came back) has nothing to do with that baby.
        if other.has_npc_partner() and not preg_partner_knows(other) and (not _mom or child_npc_is_father(other)):
            return "mom_partner" if _mom else "know_partner"
        return "mom" if _mom else "know"

    def chitchat_pregnant_friend(girl, loc, t_index, other=None):
        """`other` forces the girl she talks about (the fresh news override of label Chit_Chat)."""
        _other = other
        if _other is None:
            _targets = _preg_other_girl_targets(girl)
            if not _targets:
                return
            _other = renpy.random.choice(_targets)
        _angle = _preg_other_girl_angle(girl, _other)
        _pool = girl_pool(_PREG_OTHER_GIRL_LINES, girl, "other girl", key=_angle)
        if girl_is_mother(_other) and _angle in _PREG_OTHER_GIRL_LINES_AGAIN.get("_default", {}):
            _pool_again = girl_pool(_PREG_OTHER_GIRL_LINES_AGAIN, girl, "other girl again", key=_angle)
            if _pool_again:
                _pool = list(_pool) + list(_pool_again)
        _line = _tl(renpy.random.choice(_pool)) % dict(partner_fmt(_other), name=_other.Name)
        _jealous = (_angle in _PREG_OTHER_GIRL_HIS_ANGLES and girl.is_dating_player() and not girl.has_trait("polyamorous")
                    and _other.gid not in (getattr(girl, "harem_accepted", None) or set()))
        set_scene_expression(girl, _PREG_OTHER_GIRL_EXPR["jealous" if _jealous else _angle])
        Say_Line(girl, _line)
        # once for the belly, once more for the born baby (both prefixes are wiped by children_forget)
        _flag = ("child_gossip_jealous_%s" if girl_is_mother(_other) else "preg_gossip_jealous_%s") % _other.gid
        if _jealous and not girl.get_flag(_flag):
            girl.set_flag(_flag, True)
            Change_Status(girl, "Jealousy", _PREG_OTHER_GIRL_JEALOUSY, max_val=1000)
        if _preg_other_girl_state(_other) in ("in_labor", "mom"):
            girl.set_flag(_mom_news_flag(_other), True)     # said once: the fresh news override will not repeat it
        set_scene_expression(girl, "normal")
        print("[PREGNANCY] chitchat pregnant_friend: %s about %s (%s, stage %d) angle=%s jealous=%s forced=%s" % (
            girl.gid, _other.gid, _preg_other_girl_state(_other), getattr(_other, "_pregnancy_stage", 0), _angle, _jealous, other is not None))

    def _mom_news_flag(other):
        """One comment per pair while she is away giving birth, one more once she is back with the baby."""
        return ("child_news_labor_%s" if getattr(other, "_giving_birth", False) else "child_news_back_%s") % other.gid

    def _mom_news_target(girl):
        """FRESH news at the top of label Chit_Chat: a girl who is giving birth right now, or who came back a
        mother in the last _MOM_NEWS_DAYS days, that this speaker has not commented on yet. Returns her gid
        or None. Face to face only; rolls _MOM_NEWS_CHANCE per chat (without it the news would only be heard
        weeks later: a topic plays once per cycle of all her topics)."""
        if getattr(store, "_phone_mode", False):
            return None
        _fresh = []
        for _o in _preg_other_girl_targets(girl):
            _state = _preg_other_girl_state(_o)
            if _state == "showing":
                continue
            if _state == "mom" and (child_age_days(_o) or 0) > _BIRTH_AWAY_DAYS + _MOM_NEWS_DAYS:
                continue
            if not girl.get_flag(_mom_news_flag(_o)):
                _fresh.append(_o)
        if not _fresh or renpy.random.random() >= _MOM_NEWS_CHANCE:
            return None
        return renpy.random.choice(_fresh).gid

    def _mom_news_play(girl, other_gid, loc, t_index):
        chitchat_pregnant_friend(girl, loc, t_index, other=GIRL_BY_ID[other_gid])     # it marks the news as told

    register_chitchat("global", chitchat_pregnant_friend,
        condition=lambda g, loc, t: bool(_preg_other_girl_targets(g)), weight=3)

# ==============================================================
# MAIN ENTRY LABEL
# ==============================================================

label Chit_Chat(girl=0, loc="campus", t_index=0):

    if not girl:
        "You try to chat, but no one really answers."
        return

    # Jealousy snippy override (50% chance when >= 300)
    python:
        _jeal_override = False
        if girl.is_dating_player() and getattr(girl, "Jealousy", 0) >= 300 and renpy.random.random() < 0.5:
            if not girl.has_trait("polyamorous"):
                _jeal_override = True
    if _jeal_override:
        python:
            _jeal_val = getattr(girl, "Jealousy", 0)
            if _jeal_val >= 600:
                _jeal_snippy = [
                    _("Don't talk to me right now. I've seen enough of you with OTHER people today."),
                    _("Oh, NOW you want to chat with me? After spending all that time with her?"),
                    _("I'm really not in the mood. You know exactly why."),
                    _("Every time I turn around, you're with someone else. It's getting old."),
                ]
            else:
                _jeal_snippy = [
                    _("Hey... you've been hanging out with a lot of girls lately. Just saying."),
                    _("I saw you with her earlier. I'm not mad, just... noticing things."),
                    _("Do you even realize how much time you spend with other girls?"),
                    _("I'm trying not to be that girlfriend, but you're making it really hard."),
                ]
            set_scene_expression(girl, "angry")
            Say_Line(girl, _tl(renpy.random.choice(_jeal_snippy)))
            set_scene_expression(girl, "normal")
            girl.RegisterAction("chitchat")
        call Apply_Time_Cost(TIME_COSTS["chat"]) from _call_Apply_Time_Cost_10a
        return

    # Harem rivalry override: snide comments about a rival she dislikes
    python:
        _rivalry_override = False
        _rivalry_rival = None
        _rivalry_like = 999
        if girl.is_dating_player() and not girl.has_trait("polyamorous"):
            _r_harem = getattr(girl, "harem_accepted", None) or set()
            for _r_gid in _r_harem:
                _r_girl = GIRL_BY_ID.get(_r_gid)
                if not _r_girl or not _r_girl.is_dating_player():
                    continue
                _r_gl = girl.get_like_for(_r_gid)
                if _r_gl < 300 and _r_gl < _rivalry_like:
                    _rivalry_like = _r_gl
                    _rivalry_rival = _r_girl
            if _rivalry_rival:
                if _rivalry_like < 100:
                    _rivalry_override = renpy.random.random() < 0.80
                elif _rivalry_like < 200:
                    _rivalry_override = renpy.random.random() < 0.50
                else:
                    _rivalry_override = renpy.random.random() < 0.25
    if _rivalry_override and _rivalry_rival:
        python:
            _rn = _rivalry_rival.Name
            if _rivalry_like < 100:
                _rivalry_pool = [
                    _("I HATE %s. You know that, right? I'm only here because of you."),
                    _("%s makes my skin crawl. How can you even touch her?"),
                    _("One of us has to go. And it's not going to be me."),
                    _("I dream about the day you dump %s. Seriously."),
                ]
            elif _rivalry_like < 200:
                _rivalry_pool = [
                    _("I can barely stand being in the same room as %s."),
                    _("If you mention %s one more time, I swear..."),
                    _("I agreed to this arrangement. I didn't agree to LIKE her."),
                    _("Every time I see %s, I wonder why I'm doing this."),
                ]
            else:
                _rivalry_pool = [
                    _("I don't know what you see in %s, honestly."),
                    _("%s and I... we tolerate each other. For your sake."),
                    _("I'm not going to pretend %s and I are best friends. We're not."),
                    _("Just so you know, %s and I had a... disagreement yesterday."),
                ]
            _rivalry_line = _tl(renpy.random.choice(_rivalry_pool)) % _rn
            set_scene_expression(girl, "angry")
            Say_Line(girl, _rivalry_line)
            set_scene_expression(girl, "normal")
            girl.RegisterAction("chitchat")
        call Apply_Time_Cost(TIME_COSTS["chat"]) from _call_Apply_Time_Cost_rivalry
        return

    # Fresh baby news override: another girl is giving birth right now, or just came back a mother
    # (once per pair and per moment, _mom_news_target)
    $ _mom_news_gid = _mom_news_target(girl)
    if _mom_news_gid is not None:
        python:
            _mom_news_play(girl, _mom_news_gid, loc, t_index)
            girl.RegisterAction("chitchat")
        $ renpy.fix_rollback()
        call Apply_Time_Cost(TIME_COSTS["chat"]) from _call_Apply_Time_Cost_momnews
        return

    # A nerd gets carried away (small chance, nerd_ramble.rpy): she talks for most of the slot, it pays its own time
    if nerd_ramble_roll(girl):
        call _nerd_ramble(girl) from _call_nerd_ramble
        return

    $ _set_standing_arm(girl, renpy.random.choice([1, 1, 3]))

    python:
        if store._phone_is_open:
            print("[CHITCHAT] WARNING: _phone_is_open is True during chitchat topic — choice screen would be hidden!")
        func = pick_chitchat_func(girl, loc, t_index)
        if func in _CHITCHAT_HAS_MENU and store._phone_is_open:
            print("[CHITCHAT] CRITICAL: menu topic '%s' picked while _phone_is_open=True — forcing reset" % getattr(func, "__name__", "?"))
            store._phone_is_open = False
        func(girl, loc, t_index)
        # Track total chitchat interactions per girl
        girl.RegisterAction("chitchat")

    $ _set_standing_arm(girl, 0)

    # Fix rollback so scrolling back replays the same chitchat
    $ renpy.fix_rollback()

    call Apply_Time_Cost(TIME_COSTS["chat"]) from _call_Apply_Time_Cost_10

    return
