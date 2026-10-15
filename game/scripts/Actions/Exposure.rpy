init -998 python:
    # ------------------------------------------------------------
    # Simple exposure helper (legacy)
    # ------------------------------------------------------------
    def _register_simple_exposure(girl, key):
        """
        key: "saw_boobs" or "saw_pussy"
        Increments girl.Exposure[key] and registers tags in
        Recent_Actions / Daily_Actions.

        Returns:
            {
                "first_time": bool,
                "total": int,   # total times this exposure happened
            }
        """
        if not hasattr(girl, "Exposure"):
            return {"first_time": False, "total": 0}

        prev = girl.Exposure.get(key, 0)
        first_time = (prev == 0)

        girl.Exposure[key] = prev + 1
        total = girl.Exposure[key]

        if hasattr(girl, "Recent_Actions"):
            girl.Recent_Actions.append(key)
        if hasattr(girl, "Daily_Actions"):
            girl.Daily_Actions.append(key)

        return {"first_time": first_time, "total": total}

    # ============================================================
    # Action Registry System
    # ============================================================

    # ------------------------------------------------------------
    # RegisterAction... generic action registration
    # ------------------------------------------------------------
    def RegisterAction(self, action, amount=1):
        """
        Increment self.ActionLog[action] by amount.
        Creates the key if it doesn't exist.
        Logs the action tag in Recent_Actions / Daily_Actions.

        Returns:
            {"first_time": bool, "total": int}
        """
        if not hasattr(self, "ActionLog"):
            self.ActionLog = {}

        prev = self.ActionLog.get(action, 0)
        first_time = (prev == 0)

        self.ActionLog[action] = prev + amount
        total = self.ActionLog[action]

        if hasattr(self, "Recent_Actions"):
            self.Recent_Actions.append(action)
        if hasattr(self, "Daily_Actions"):
            self.Daily_Actions.append(action)

        return {"first_time": first_time, "total": total}

    # ------------------------------------------------------------
    # HasSeen... quick boolean check
    # ------------------------------------------------------------
    def HasSeen(self, action):
        """Returns True if action was registered at least once."""
        if not hasattr(self, "ActionLog"):
            return False
        return self.ActionLog.get(action, 0) > 0

    # ------------------------------------------------------------
    # GetActionCount... read count
    # ------------------------------------------------------------
    def GetActionCount(self, action):
        """Returns how many times action was registered."""
        if not hasattr(self, "ActionLog"):
            return 0
        return self.ActionLog.get(action, 0)

    # ------------------------------------------------------------
    # CheckClothingExposure... check current clothing and register
    # ------------------------------------------------------------
    def CheckClothingExposure(self):
        """
        Checks current clothing state and registers exposure if body
        parts are visible.

        - Over is None AND Chest is None -> player_saw_boobs
        - Legs is None AND Panties is None -> player_saw_pussy

        Returns:
            {
                "saw_boobs": bool,       # visible right now
                "saw_pussy": bool,       # visible right now
                "first_boobs": bool,     # was first time
                "first_pussy": bool,     # was first time
                "total_boobs": int,      # total times seen
                "total_pussy": int,      # total times seen
            }
        """
        # Boobs visible: no over AND mid not covering AND (no chest OR chest displaced up)
        _chest_exposed = self.Chest is None or self.clothes_state.get("chest") == "up"
        _mid_hides = self.Mid is not None and not self.MidUp
        saw_boobs = (self.Over is None and not _mid_hides and _chest_exposed)
        # Pussy visible: no skirt/panties OR panties displaced (side/down)
        _pan_state = self.clothes_state.get("panties", "full")
        _pan_exposed = self.Panties is None or _pan_state in ("side", "down")
        _skirt_ok = self.Legs is None or self.clothes_state.get("skirt") == "up"
        saw_pussy = (_skirt_ok and _pan_exposed)
        first_boobs = False
        first_pussy = False
        total_boobs = self.GetActionCount("player_saw_boobs")
        total_pussy = self.GetActionCount("player_saw_pussy")

        if saw_boobs:
            result = self.RegisterAction("player_saw_boobs")
            first_boobs = result["first_time"]
            total_boobs = result["total"]

        if saw_pussy:
            result = self.RegisterAction("player_saw_pussy")
            first_pussy = result["first_time"]
            total_pussy = result["total"]

        return {
            "saw_boobs": saw_boobs,
            "saw_pussy": saw_pussy,
            "first_boobs": first_boobs,
            "first_pussy": first_pussy,
            "total_boobs": total_boobs,
            "total_pussy": total_pussy,
        }

    # ------------------------------------------------------------
    # MarkGirlSawPenis... girl saw the player's penis
    # ------------------------------------------------------------
    def MarkGirlSawPenis(self):
        """Register that this girl saw the player's penis."""
        return self.RegisterAction("girl_saw_penis")

    # ------------------------------------------------------------
    # MarkCaughtInAct... player caught girl in an act
    # ------------------------------------------------------------
    def MarkCaughtInAct(self, act):
        """
        Register that the player caught this girl in an act,
        and also check clothing exposure.

        Returns:
            {"act": {"first_time": bool, "total": int},
             "exposure": {"saw_boobs": bool, ...}}
        """
        act_result = self.RegisterAction(act)
        exposure_result = self.CheckClothingExposure()
        return {"act": act_result, "exposure": exposure_result}

    # ------------------------------------------------------------
    # API – player saw boobs (legacy + ActionLog sync)
    # ------------------------------------------------------------
    def MarkSawBoobs(self):
        """
        Call whenever the player sees this girl's boobs.
        Maintains legacy Exposure dict AND syncs to ActionLog.

        Example:
            $ result = girl.MarkSawBoobs()
            if result["first_time"]:
                # run first-time topless scene
                call Gwen_First_Topless_FirstTime(girl)
        """
        self.RegisterAction("player_saw_boobs")
        return _register_simple_exposure(self, "saw_boobs")

    # ------------------------------------------------------------
    # API – player saw pussy (legacy + ActionLog sync)
    # ------------------------------------------------------------
    def MarkSawPussy(self):
        """
        Call whenever the player sees this girl's pussy.
        Maintains legacy Exposure dict AND syncs to ActionLog.

        Example:
            $ result = girl.MarkSawPussy()
            if result["first_time"]:
                # run first-time bottomless scene
                call Gwen_First_Bottomless_FirstTime(girl)
        """
        self.RegisterAction("player_saw_pussy")
        return _register_simple_exposure(self, "saw_pussy")

    # ------------------------------------------------------------
    # Bind all methods into Girl
    # ------------------------------------------------------------
    Girl.RegisterAction = RegisterAction
    Girl.HasSeen = HasSeen
    Girl.GetActionCount = GetActionCount
    Girl.CheckClothingExposure = CheckClothingExposure
    Girl.MarkGirlSawPenis = MarkGirlSawPenis
    Girl.MarkCaughtInAct = MarkCaughtInAct
    Girl.MarkSawBoobs = MarkSawBoobs
    Girl.MarkSawPussy = MarkSawPussy

# ============================================================
# CheckExposure... wrapper that checks clothing + triggers
# first-time reaction automatically
# ============================================================
# Usage:
#   call CheckExposure(girl)
# ============================================================

label CheckExposure(girl):
    $ _exposure = girl.CheckClothingExposure()

    if _exposure["first_boobs"]:
        call FirstExposureReaction(girl, "boobs") from _call_FirstExposureReaction

    if _exposure["first_pussy"]:
        call FirstExposureReaction(girl, "pussy") from _call_FirstExposureReaction_1

    return _exposure

# ============================================================
# First-time exposure reaction scene
# ============================================================
# Called automatically when player sees boobs or pussy for
# the first time. Girl asks if you like what you see.
#
# Usage:
#   call FirstExposureReaction(girl, "boobs")
#   call FirstExposureReaction(girl, "pussy")
# ============================================================

label FirstExposureReaction(girl, part):

    # Check if player is behind her (doggy/RCG) — can't see from there
    $ _is_from_behind = getattr(store, "_doggy_girl", None) is not None or getattr(store, "_rcg_girl", None) is not None

    $ _fer_femdom = hasattr(girl, "has_trait") and girl.has_trait("femdom")

    if part == "boobs":
        if _is_from_behind:
            if _fer_femdom:
                $ Say_Line(girl, _("I show you these for the first time and you can't even see them from back there. Typical."))
            else:
                $ Say_Line(girl, _("What a waste... I get them out for the first time and you can't even see them from there."))
            $ girl.RegisterAction("player_saw_boobs")
            $ Change_Status(girl, "Inbt", 10)
        elif _fer_femdom:
            $ Say_Line(girl, _("I know these are the best you'll ever see in your life. So close your mouth."))

            menu:
                "They really are...":
                    $ Change_Status(girl, "Love", 15)
                    $ Say_Line(girl, _("Hmph. At least you know quality when you see it."))

                "Yes ma'am.":
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Say_Line(girl, _("Good. Now stop drooling."))

                "Make me.":
                    $ Change_Status(girl, "Inbt", 20)
                    $ Change_Status(girl, "Obed", 10)
                    $ Say_Line(girl, _("Oh... you've got nerve. I like that."))
        else:
            $ Say_Line(girl, _("You're staring at my chest... Do you like what you see?"))

            menu:
                "You're beautiful...":
                    $ Change_Status(girl, "Love", 15)
                    $ Say_Line(girl, _("That's... really sweet of you."))

                "I do. And you should show me more often.":
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Say_Line(girl, _("I... okay, if you say so."))

                "You've got nothing to be shy about.":
                    $ Change_Status(girl, "Inbt", 20)
                    $ Change_Status(girl, "Obed", 10)
                    $ Say_Line(girl, _("Heh... maybe I don't."))

    else:
        if _fer_femdom:
            $ Say_Line(girl, _("Eyes up here. Or down there. Pick one, but stop gawking like you've never seen one."))

            menu:
                "Hard not to stare...":
                    $ Change_Status(girl, "Love", 15)
                    $ Say_Line(girl, _("Hmph. At least you know quality when you see it."))

                "Sorry, I just...":
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Say_Line(girl, _("You should be. Now get a grip."))

                "Oh, I plan to keep looking.":
                    $ Change_Status(girl, "Inbt", 20)
                    $ Change_Status(girl, "Obed", 10)
                    $ Say_Line(girl, _("We'll see about that."))
        else:
            $ Say_Line(girl, _("You're looking down there... Do you like what you see?"))

            menu:
                "Beautiful...":
                    $ Change_Status(girl, "Love", 15)
                    $ Say_Line(girl, _("That's... really sweet of you."))

                "Finally...":
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Say_Line(girl, _("I... okay, if you say so."))

                "First of many...":
                    $ Change_Status(girl, "Inbt", 20)
                    $ Change_Status(girl, "Obed", 10)
                    $ Say_Line(girl, _("Heh... maybe I don't."))

    return

# ============================================================
# Caught exposure reaction (shower, bedroom, etc.)
# ============================================================
# Called when the player catches the girl exposed in a non-sex
# context (e.g. walking in on her). Stat gains scale with
# the girl's current level and low stats cause side-effects.
#
# Usage:
#   call CaughtExposureReaction(girl, "boobs")
#   call CaughtExposureReaction(girl, "pussy")
# ============================================================

label CaughtExposureReaction(girl, part):

    python:
        _has_t = hasattr(girl, "has_trait") and girl.has_trait
        _is_exhib = _has_t and girl.has_trait("exhibitionist")
        _is_cute = _has_t and girl.has_trait("cute_sex")
        _is_hc = _has_t and girl.has_trait("hardcore_sex")
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _inbt = getattr(girl, "Inbt", 0)
        _love = getattr(girl, "Love", 0)

        if _is_exhib:
            if part == "boobs":
                _open_lines = [
                    _("Like what you see? I don't mind you looking."),
                    _("Oh, you caught me. I'm not going to cover up though."),
                    _("Take a good look. I'm not shy about these."),
                ]
            else:
                _open_lines = [
                    _("Well, now you've seen everything. Happy?"),
                    _("I could cover up... but where's the fun in that?"),
                    _("You're staring. I don't mind."),
                ]
        elif _is_cute:
            if part == "boobs":
                _open_lines = [
                    _("Eek! D-don't look! I wasn't ready!"),
                    _("Oh no, oh no, oh no... you saw them..."),
                    _("This is so embarrassing... please look away..."),
                ]
            else:
                _open_lines = [
                    _("AH! No! Don't look down there!"),
                    _("I... I can't believe you saw that... I want to disappear..."),
                    _("This is the worst... please just... forget what you saw..."),
                ]
        elif _is_hc:
            if part == "boobs":
                _open_lines = [
                    _("Enjoyed the show? That was the last act."),
                    _("I hope you got a good look. That's all you're getting."),
                    _("Staring? I don't blame you. They're worth staring at."),
                ]
            else:
                _open_lines = [
                    _("Caught me. So what? Not like you haven't thought about it."),
                    _("If you're going to look, at least have the guts to admit you liked it."),
                    _("Well? Are you just going to stand there or do something about it?"),
                ]
        elif _has_bf:
            if part == "boobs":
                _open_lines = [
                    _("My %(pl)s would kill you for seeing that... but %(pp)s's not here."),
                    _("You shouldn't have seen those... I have a {hint}%(pl)s{/hint}, you know."),

                    _("Great. Now you've seen more of me than you should have..."),
                ]
            else:
                _open_lines = [
                    _("If my {hint}%(pl)s{/hint} knew you just saw that... ugh."),

                    _("You saw nothing. NOTHING. My {hint}%(pl)s{/hint} can never know."),

                    _("This never happened. Understood?"),
                ]
        elif _inbt >= 400:
            if part == "boobs":
                _open_lines = [
                    _("Well, I guess there's no point covering up now, is there?"),
                    _("I hope the view was worth it. I'm not exactly hiding anymore."),
                    _("Enjoying the scenery? I'm used to it at this point."),
                ]
            else:
                _open_lines = [
                    _("I guess modesty is overrated anyway."),
                    _("You've seen worse. Or better, depending on your perspective."),
                    _("At this point, I've stopped being surprised by these situations."),
                ]
        elif _love >= 400:
            if part == "boobs":
                _open_lines = [
                    _("I... I didn't want you to see them like this. Not yet, anyway."),
                    _("You saw... well. I guess it was going to happen eventually."),
                    _("Don't get any ideas... but I'm not mad you saw."),
                ]
            else:
                _open_lines = [
                    _("I can't believe you saw that... but if it had to be anyone..."),
                    _("Well. That's one way to move our relationship forward."),
                    _("I'm embarrassed... but I trust you. Don't make me regret it."),
                ]
        else:
            if part == "boobs":
                _open_lines = [
                    _("I hope the view was worth it for you."),
                    _("Hey! A little privacy?! You can't just walk in like that!"),
                    _("Great. Now you've seen my chest. Feel proud of yourself?"),
                ]
            else:
                _open_lines = [
                    _("I hope the view was worth it for you."),
                    _("Do you just not understand the concept of KNOCKING?!"),
                    _("I cannot believe this just happened..."),
                ]

    $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_open_lines))))

    menu:
        "It was a nice surprise for me.":
            $ _lv = getattr(girl, "Love", 0)
            if _lv >= 500:
                $ Change_Status(girl, "Love", 20)
                $ Say_Line(girl, _("That's... actually really sweet."))
            elif _lv >= 200:
                $ Change_Status(girl, "Love", 15)
                $ Change_Status(girl, "Inbt", 5)
                $ Say_Line(girl, _("At least you're honest about it."))
            else:
                $ Change_Status(girl, "Love", 10)
                $ Say_Line(girl, _("Sweet words don't fix everything, you know."))

        "I don't regret anything.":
            $ _ob = getattr(girl, "Obed", 0)
            if _ob >= 500:
                $ Change_Status(girl, "Obed", 25)
                $ Say_Line(girl, _("I... guess I wouldn't expect anything else from you."))
            elif _ob >= 200:
                $ Change_Status(girl, "Obed", 18)
                $ Change_Status(girl, "Inbt", 8)
                $ Say_Line(girl, _("You really have no shame, do you?"))
            else:
                $ Change_Status(girl, "Obed", 12)
                $ Change_Status(girl, "Inbt", 5)
                $ Say_Line(girl, _("Wow. You could at least pretend to be sorry."))

        "It's something natural, no big deal.":
            $ _ib = getattr(girl, "Inbt", 0)
            if _ib >= 500:
                $ Change_Status(girl, "Inbt", 25)
                $ Say_Line(girl, _("You're right... it's no big deal."))
            elif _ib >= 200:
                $ Change_Status(girl, "Inbt", 18)
                $ Change_Status(girl, "Obed", 8)
                $ Say_Line(girl, _("I suppose you have a point..."))
            else:
                $ Change_Status(girl, "Inbt", 12)
                $ Change_Status(girl, "Obed", 5)
                $ Say_Line(girl, _("Easy for you to say! I'm the one exposed here!"))

    return

# ============================================================
# Player exposes himself... girl sees penis for the first time
# ============================================================
# Called from sex scene Launch labels. Registers the action,
# and if first time, shows the girl's surprised reaction +
# gives Inbt bonus.
#
# Usage:
#   call PlayerExposure(girl)
# ============================================================

label PlayerExposure(girl):

    # Already exposed this sex session (position switch)... skip
    if getattr(store, "_player_exposed_this_session", False):
        return

    $ store._player_exposed_this_session = True

    "You drop your pants and expose yourself."

    # Track sex-scene exposure separately (shower/dares don't count)
    $ _exp_penis = girl.RegisterAction("girl_saw_penis")
    $ _sex_exp = girl.RegisterAction("girl_saw_penis_sex")

    if _sex_exp["total"] == 1:
        # First time seeing it in a sexual context. A girl whose ROLE carries its own first-sight pool
        # speaks that instead (the stepmom measures him against her husband; author 2026-10-10:
        # "maior que o do pai"): girl -> role -> nothing, then the shared pools below.
        $ _penis_role_line = rod_pick_line(girl, "penis_first_sight", default=None)
        if _penis_role_line:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _penis_role_line)
        elif _exp_penis["total"] == 1:
            # Never seen it at all — full surprise
            $ set_scene_expression(girl, "surprised")
            python:
                _penis_lines = [
                    _("Oh my... you're bigger than I expected."),
                    _("Wow... that's... impressive."),
                    _("I wasn't expecting... all of that."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_penis_lines)))
        else:
            # Saw it before (shower/dares/walk-in) but first time in sexual context
            $ set_scene_expression(girl, "surprised")
            python:
                _penis_lines = [
                    _("It looks even bigger up close like this..."),
                    _("I've seen it before, but... this feels different."),
                    _("Seeing it is one thing, but up close like this..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_penis_lines)))

        $ Change_Status(girl, "Inbt", 50)
        $ Change_Status(girl, "Obed", 15)

    elif _sex_exp["total"] == 2:
        if getattr(store, "_coercion_type", None):
            $ Say_Line(girl, renpy.random.choice([_("Here we go again..."), _("I know what you want."), _("...Just get it over with.")]))
        else:
            $ Say_Line(girl, renpy.random.choice([_("Almost forgot how big this is..."), _("There it is again... still impressive."), _("Mmm... I missed this.")]))

    elif _sex_exp["total"] >= 3:
        if getattr(store, "_coercion_type", None):
            $ Say_Line(girl, renpy.random.choice([_("..."), _("I already know the drill."), _("Fine. Let's just do this.")]))
        else:
            $ Say_Line(girl, renpy.random.choice([_("Heh, I never get tired of seeing this."), _("Hello, old friend..."), _("I know what's coming next...")]))

    return
